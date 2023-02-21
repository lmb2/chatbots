# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 10:50:18 2022

@author: Laura-Marie Behmenburg und Fabian van Treek
"""
import random
import json
import pickle
import numpy as np
import spacy
import tasks_hope

from tensorflow.keras.models import load_model

nlp = spacy.load("en_core_web_lg")

intents = json.loads(open('data/intents_hope.json',encoding='utf8').read())

words = pickle.load(open('data/words_intents.pkl', 'rb'))
classes = pickle.load(open('data/classes_intents.pkl', 'rb'))
model = load_model('data/chatbotmodelintents.h5')

'''
Dictionary mit Angaben wann Informationen aus dem Input zur weiteren Nutzung gezogen werden sollen
Schema: "Tag: ([parameter_name_to_change,splitTrigger],[entity_names_to_check_for])"
-> parameter_name_to_change: Angabe wird in Response(Intent) entsprechend ersetzt
-> splittTrigger: Gibt an ob und wie eine Eingabe aufgeteilt werden soll
-> entity_names_to_check_for: Gewünschte Tags die zu überprüfen sind mittels Spacy-Inhalts Check
'''
get_information_dict = {
    "courtesyGreetingResponse": (["<HUMAN>",""],["PERSON","ORG","NORP"]),
    "weather": (["<>",""],["PERSON","ORG","GPE","EVENT"]),
    "wikipediaSearch": (["<>","split"],["about","for"]),
    "google": (["<>","pure"],[""])
    }

'''
Dictionary zum Angeben der auszuführenden Tasks und deren Trigger(Response)
Schema: "Response: function_name"
'''
task_dict = {
    "Redirecting to Google...": "do_google_search",
    "Date and Time": "do_current_date_and_time",
    "Date": "do_current_date",
    "Time": "do_current_time",
    "Weather": "do_weather_in",
    "WikiSearch": "do_wikipedia_search"
              }

'''
Dictionary zum Angeben von direkten Reaktion des Bots auf eine Eingabe, basierend auf vorheriger Antwort(Tag) des Bots
Schema: "Tag: (newResponseTag,[latestMemoryTagsTriggers])"
-> Tag: Tag des Intents welcher initial durch den User-Input getriggert wird
-> newResponseTag: Setzen eines neuen Tag-Namens welcher dann auch im Speicher der letzten Botnachrichten gespeichert wird
-> latestMemoryTagsTriggers: Liste mit allen letzten im Speichern vorhandenen Tags die die Reaktion triggern sollen 
'''
direct_response_dict = {
    "wrongAnswer": ("wrongAnswerResponse",["wikipediaSearch"]),
    "anotherJoke": ("jokes",["jokes"]),
    "anotherRiddle": ("riddle",["riddle"])
    }

'''
Dictionary zum Angeben ob die User-Eingabe welche nach einem direct-response getätigt wurde eine andere Reaktion auslöst
Schema: "latestMemoryTag: {lastButOneMemoryTag: reponseTriggerForTaskDict}"
-> latestMemoryTag: Angabe des Direct-Repsponse-Tags welche die Atkion auslösen kann
-> lastButOneMemoryTag: Vorletzter gesendeter Tag des Bots der >ReponseTriggerForTaskDirct< auslöst
-> responseTiggerForTaskDict: Response die entsprechend dem task_dict die gewünschte Aufgabe ausführt
'''
direct_task_with_input = {
    "wrongAnswerResponse": {"wikipediaSearch": "WikiSearch"}
    }

'''
Liste mit den Tags welche beim Triggern zusätzlich mit Spacy abgeglichen werden sollen
    -> Model liefert Tag dessen Responses inhaltlich nicht zur User-Eingabe passen
        => google_serach trigger
'''
spacy_content_check = [
    "location",
    "fact-21"
    ]

ignore_letters = ['?', '!', '.', ',']
latest_response_memory = []

'''
Eingabe tokenizen und lemmatizen
'''
def clean_up_sentence(sentence):
    doc = nlp(sentence)
    sentence_words = []
    for token in doc:
        if token.lemma_ not in ignore_letters:
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
Vergleicht inhaltlich alle vorhandenen Pattern in der übermittelten Klasse/Tag mit dem übermittelten Satz/Eingabe
return True => geringe inhaltliche Übereinstimmung der Pattern mit Eingabe
return False => hohe inhaltliche Übereinstimmung der Pattern mit Eingabe
'''
def content_pattern_check(predicted_class,sentence):
        tag_to_check_pattern = predicted_class[0]['intent']
        list_of_intents = intents['intents']      
        patterns_to_check = []
        highest_similartiy = 0;
        for i in list_of_intents:
            if i['tag'] == tag_to_check_pattern:
                patterns_to_check = i['patterns']
        
        for pattern in patterns_to_check:
            simi = nlp(pattern).similarity(nlp(sentence))
            if simi > highest_similartiy:
                highest_similartiy = simi
        
        if highest_similartiy < 0.9:
            return True
        else:
            return False
            
'''
Prüfen/Herausfinden für welche Klasse(Tag) die Eingabe zutrifft/passend ist
'''
def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]),verbose=0)[0]
    ERROR_THRESHOLD = 0.3 #Welche Überstimmung mindestens vorhaden sein muss
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True) #Sortierung das höchste Wahrscheinlichkeit an erster Stelle steht
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    
    '''
    Falls keine Übereinstimmung gefunden wurde, wird als default "google" gesetzt => Usereingabe wird gegoogelt
    Außerdem wird geprüft ob die aktuelle höchste übereinstimmende Klasse/Tag in der content_check Liste vorhanden ist
    (Dient der Abgrenzung inhaltlicher Konflikte, z.B. Triggern fragen nach Orte häufig "locatin" des Bots, obwohl nach Orten gefragt wird)
        -> Falls ja => Prüfen lassen der inhaltlichen Übereinstimmung der Eingabe zu den Pattern der Klasse/Tag
            -> Stellt sich geringe inhaltliche Übereinstimmung heraus => setzten des "google"-Triggers um Usereingabe zu googeln
    '''
    if len(return_list) == 0:
        return_list.append({'intent': "google", 'probability': str(1.0)})
    elif return_list[0]['intent'] in spacy_content_check:
        if (content_pattern_check(return_list, sentence)):
            return_list.insert(0,{'intent': "google", 'probability': str(1.0)})
        
    #print(return_list)#Kann zur Ausgabe der Übersicht der getriggerten Tags genutzt werden
    return return_list

'''
Methode zum Herausfiltern von konkreten Informationen für die weiter Verwendung
Bestimmt durch Angabe bestimmter Parameter
Entweder ein Triggerword ist angegeben z.B. split -> mit zugehörigen Werten
    -> dann wird der entsprechende Part in der Methode ausgeführt
Oder es findet regulärer Aufruf statt, mit angabe der Entitys nach den Spacys suchen/filtern soll
'''
def get_information(tag, message):
    if get_information_dict.get(tag)[0][1] == "split":
        split_words_to_check_for = get_information_dict.get(tag)[1]
        message_words = clean_up_sentence(message)
        for splitter in split_words_to_check_for:
            for elem in message_words:
                if splitter == elem:
                    index_of_elem = message_words.index(elem)
                    return_value = list(message_words)[index_of_elem+1:]
                    break
    elif get_information_dict.get(tag)[0][1] == "pure":
        return message
    else:
        entity_names_to_check_for = get_information_dict.get(tag)[1]
        doc = nlp(message)
        entities=[(i, i.label_) for i in doc.ents if i.label_ in entity_names_to_check_for]
        if len(entities) != 0:
            return_value = str(entities[0][0])
    '''
    Wenn return_value Variable nicht gefüllt werden konnte existiert sie nicht!
    Wir dann im except abgefangen und ein default-Rückgabewert gesetzt
    '''
    try:
        return_value
    except NameError:
        return_value = "dontknow"
            
    return return_value

'''
Speichern der letzten Nachricht im Memory(Gedächtnis) des Bots
-> wenn mehr als 3 gespeichert sind wird älteste gelöscht => immer nur 3 letzte Nachrichten vorhanden
'''
def safe_in_memory(tag,response):
    global latest_response_memory
    latest_response_memory.append((tag,response))
    if len(latest_response_memory) > 3:
        latest_response_memory = list([entry for entry in latest_response_memory if latest_response_memory.index(entry) > 0])
        
'''
Ausgabe des letzten im Speicher vorhandenen Eintrags
'''        
def get_last_memory_tag():
    global latest_response_memory
    if len(latest_response_memory)>0:
        return latest_response_memory[-1][0]
    else:
        return 0

'''
Ausgabe des vorletzten im Specher vorhandenen Eintrags
'''
def get_last_but_one_memory_tag():
    global latest_response_memory
    if len(latest_response_memory)>1:
        return latest_response_memory[-2][0]
    else:
        return 0
    
'''
Antwort aus User-Input bestimmen
Herausfiltern der wahrscheinlichsten Response über die predict_class-Methode
Wählen einer zufälligen Antwort aus den möglichen Reponses wenn keine Sonderfälle eintreten
'''
def get_response(message):
    '''
    Checken ob letzte gesendete Response Teil vom direct Response (Rückfragen des Bots) sind 
    und vom direct task => aktuelle User-Eingabe bezieht sich auf letzte Response des Bots und hat task-Aufruf 
    '''
    if get_last_memory_tag() != 0 and get_last_memory_tag() in direct_task_with_input.keys():
        possible_actions = direct_task_with_input.get(get_last_memory_tag())
        if get_last_but_one_memory_tag() in possible_actions.keys():
            key_of_possible_action = get_last_but_one_memory_tag()
            value_of_possible_action = possible_actions.get(get_last_but_one_memory_tag())
            if key_of_possible_action in get_information_dict.keys() and value_of_possible_action in task_dict.keys():
                function_name = task_dict.get(value_of_possible_action)
                function_call = eval("tasks_hope."+function_name)
                result = function_call(message,False)#Funktionsaufruf
            safe_in_memory(key_of_possible_action,result)
        else:
            result = "I think I misunderstood something."
            safe_in_memory("ERROR",result)
    else:
        predicted_class = predict_class(message)
        tag_of_highest_probability_from_predicted_classes = predicted_class[0]['intent']
        list_of_intents = intents['intents']            
        for i in list_of_intents:
            if i['tag'] == tag_of_highest_probability_from_predicted_classes:
                result = random.choice(i['responses'])
                
                '''
                Prüfen ob der Tag aus dem Response(result) bestimmt wurde Trigger für Informationsgewinnung aus User-Input ist
                    -> Information entrspchend der vorhandenen Angaben im get_information_dict auslesen lassen
                        -> Wenn keine Information gewonnen werden konnten default Antwort setzten
                        -> Wenn die zuvor bestimmte Response(result) zusätzlich Trigger für eine Aufgabe(task) ist
                            -> Funktionsaufruf durchführen
                        -> Ansonsten in zuvor bestimmter Response(result) die gewonnen Informationen einsetzten
                '''
                if tag_of_highest_probability_from_predicted_classes in get_information_dict.keys():
                    to_change = get_information(tag_of_highest_probability_from_predicted_classes, message)
                    change_parameter = get_information_dict.get(tag_of_highest_probability_from_predicted_classes)[0][0]
                    if to_change == "dontknow":
                        result = "I don't understand."
                    elif result in task_dict.keys():
                        function_name = task_dict.get(result)
                        function_call = eval("tasks_hope."+function_name)
                        result = function_call(to_change)
                    else:
                        result = result.replace(change_parameter,to_change)
                        
                '''
                Prüfen ob !!!keine!!! Bedigung vorliegt das Informationen ausgelesen werden sollen
                        -> um doppelt aufruf zu verhinden für den Fall:
                            -> information auslese wird getriggert und zusätzlich methoden aufruf mit parameter
                Prüfen ob die Response ein Trigger im task_dict ist 
                falls ja -> aufrufen der entsprechenden Methode die den Task bearbeitetet 
                '''
                if tag_of_highest_probability_from_predicted_classes not in get_information_dict.keys():
                    if result in task_dict.keys():
                        function_name = task_dict.get(result)
                        function_call = eval("tasks_hope."+function_name)
                        result = function_call()
                        
                        
                '''
                Prüfen ob der bestimmte Tag für die Response(result) eine direkte Antwort auf den vorherigen User-Input hat
                '''
                if tag_of_highest_probability_from_predicted_classes in direct_response_dict.keys():
                    possible_trigger_latest_response_tags = direct_response_dict.get(tag_of_highest_probability_from_predicted_classes)[1]
                    if get_last_memory_tag() in possible_trigger_latest_response_tags:
                        response_tag = direct_response_dict.get(tag_of_highest_probability_from_predicted_classes)[0]
                        for entry in list_of_intents:
                            if entry['tag'] == response_tag:
                                result = random.choice(entry['responses'])
                                tag_of_highest_probability_from_predicted_classes = response_tag
                                break
                
                '''
                Speichern der bestimmmten, gesendeten Response des Bots in eine Liste. Diese enthällt immer die letzten 3 Responses.
                '''
                safe_in_memory(tag_of_highest_probability_from_predicted_classes,result)
                break
    return result

'''
Main-Methode zum Ausführen des Chatbots
'''    
def run_hope():
    print("Bot is running!")
    user_input = ""
    while user_input.lower().strip() not in ["exit", "quit", "q"]:
        user_input = input("Me: ")
        if user_input == "":
            print("You entered nothing!")
        elif user_input in ["exit", "quit", "q"]:
            break
        else:
            answer = get_response(user_input)
            print("Hope:",answer)
    print("Hope: Thanks for talking to me. Bye!")
    
'''
Codepart für das Nutzen des Chatbot-Moderators -> findet Anwendung in "chatbot_moderator_interaction.py" 
'''
def get_bot_response(user_input):
    if user_input == "":
        return "You entered nothing!"
    else:
        answer = get_response(user_input)
        return answer
    
if __name__ == '__main__':
    run_hope()