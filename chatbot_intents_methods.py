# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 10:50:18 2022

@author: Fabian
"""
import random
import json
import pickle
import numpy as np
import spacy
import tasks #ist used, aber da in " " für Aufruf genutzt erkennt die IDE das nicht

from tensorflow.keras.models import load_model

nlp = spacy.load("en_core_web_lg")

intents = json.loads(open('data/intents_big.json',encoding='utf8').read())

words = pickle.load(open('data/words_intents.pkl', 'rb'))
classes = pickle.load(open('data/classes_intents.pkl', 'rb'))
model = load_model('data/chatbotmodelintents.h5')

#Tag: (<parameter_name_to_change>,[entity_names_to_check_for])
#OR Tag:(trigger_word,[trigger_words_needed])
get_information_dict = {
    "courtesyGreetingResponse": ("<HUMAN>",["PERSON","ORG","NORP"]),
    "weather": ("<>",["PERSON","ORG","GPE","EVENT"]),
    "wikipediaSearch": ("split",["about","for"])
    }
#Response: function_name
task_dict = {
    "Redirecting to Google...": "do_google_search",
    "Date and Time": "do_current_date_and_time",
    "Date": "do_current_date",
    "Time": "do_current_time",
    "Weather": "do_weather_in",
    "WikiSearch": "do_wikipedia_search"
              }
latest_response_memory = []

def clean_up_sentence(sentence):
    doc = nlp(sentence)
    sentence_words = []
    for token in doc:
        sentence_words.append(token.lemma_)
    return sentence_words

'''
Bag of Words für die Eigabe erstellen ->
prüfen für jedes Wort der Eingabe ob es in den Wörtern(words) aus den pattern vorkommt
'''
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

'''
Prüfen/Herausfinden für welche Klasse(Tag) die Eingabe zutrifft/passend ist
'''
def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25 #Welche Überstimmung mindestens vorhaden sein muss
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    
    results.sort(key=lambda x: x[1], reverse=True) #Sortierung das höchste Wahrscheinlichkeit an erster Stelle steht
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
        
    if len(return_list) == 0:
        return_list.append({'intent': "noanswer", 'probability': str(1.0)})
        
    print(return_list)
    return return_list

'''
Methode zum herausfiltern von Konkreten informationen für die weiter Verwendung
Bestimmt durch Angabe bestimmter Parameter
Entweder ein Triggerword ist angegeben z.B. split -> mit zugehörigen Werten
    -> dann wird der entsprechende Part in der Methode ausgeführt
Oder es findet regulärer Aufruf statt, mit angabe der Entitys nach den Spacys suchen/filtern soll
'''
def get_information(tag, message):
    if get_information_dict.get(tag)[0] == "split":
        split_words_to_check_for = get_information_dict.get(tag)[1]
        for splitWord in split_words_to_check_for:
            if message.find(splitWord) != -1:
                return_value = message.split(splitWord,1)[1]
                break
    else:
        entity_names_to_check_for = get_information_dict.get(tag)[1]
        doc = nlp(message)
        entities=[(i, i.label_) for i in doc.ents if i.label_ in entity_names_to_check_for]
        #print(entities)
        
        if len(entities) == 0:
            return_value = "dontknow"
        else:
            return_value = str(entities[0][0])

    return return_value
    
'''
Antwort aus message bstimmen
Herausfiltern der wahrscheinlichsten Response über die predict class
Wählen einer zufälligen Antwort aus den möglichen Reponses
'''
def get_response(message):
    global latest_response_memory
    predicted_class = predict_class(message)
    tag_of_highest_probability_from_predicted_classes = predicted_class[0]['intent']
    list_of_intents = intents['intents']
    for i in list_of_intents:
        if i['tag'] == tag_of_highest_probability_from_predicted_classes:
            result = random.choice(i['responses'])
            
            '''
            Prüfen ob der Tag aus dem Response bestimmt wurde Teil der Tags is in dem Parameter ausgetauscht werden
            Wenn ja -> über get_information Methode die Auszutauschenden Werte holen
                        -> vorher prüfen ob aus der Eingabe die entsprechenden Infos gewonne wurden, denn falls nicht
                            -> andernfalls früfen ob funktionsaufruf existiert für den parameter gebraucht wird
                                -> Default Antwort setzen
            '''
            if tag_of_highest_probability_from_predicted_classes in get_information_dict.keys():
                to_change = get_information(tag_of_highest_probability_from_predicted_classes, message)
                change_parameter = get_information_dict.get(tag_of_highest_probability_from_predicted_classes)[0]
                if to_change == "dontknow":
                    result = "I don't understand."
                elif result in task_dict.keys():
                    function_name = task_dict.get(result)
                    function_call = eval("tasks."+function_name)
                    result = function_call(to_change)
                else:
                    result = result.replace(change_parameter,to_change)
                    
            '''
            Prüfen ob !!!keine!!! Bedigung vorliegt das Informationen ausgelesen werden sollen
                    -> um doppelt aufruf zu verhinden für den Fall:
                        -> information auslese wird getriggert und zusätzlich methoden aufruf mit parameter
            Prüfen ob die Reponse ein Trigger im task_dict ist 
            falls ja -> aufrufen der entsprechenden Methode die den Task bearbeitetet 
            '''
            if tag_of_highest_probability_from_predicted_classes not in get_information_dict.keys():
                if result in task_dict.keys():
                    function_name = task_dict.get(result)
                    function_call = eval("tasks."+function_name)
                    result = function_call()
            '''
            Speichern der bestimmmten, gesendeten Response des Bots in eine Liste. Diese enthällt immer die letzten 3 Responses.
            '''
            latest_response_memory.append(result)
            if len(latest_response_memory) > 3:
                latest_response_memory = list([entry for entry in latest_response_memory if latest_response_memory.index(entry) > 0])
            break
    return result



print("Bot is running!")

while True:
    message = input("")
    res = get_response(message)
    print(res)