# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 12:51:18 2022

@author: Fabian
"""

import spacy
nlp = spacy.load("en_core_web_lg")

pattern_sentence_1 = nlp("Where are you?")
pattern_sentence_2 = nlp("Where do i find you?")

check_sentence = nlp("where do you live?")

print(pattern_sentence_1.similarity(check_sentence))
print(check_sentence.similarity(pattern_sentence_1))

print(pattern_sentence_2.similarity(check_sentence))
print(check_sentence.similarity(pattern_sentence_2))


#import tasks

# task_dict = {
#     "Redirecting to Google...": "do_google_search",
#     "Date and Time": "do_current_date_and_time",
#     "Date": "do_current_date",
#     "Time": "do_current_time",
#     "Weather": "do_weather_in"
#               }

#function = globals()[method_dir.get("print")]
#function()


#function_name = task_dict.get("Weather")
#city = "Köln"
#function = eval("tasks."+function_name)
#print(function(city))

#print(method_dir.keys())



'''
PERSON:      People, including fictional.
NORP:        Nationalities or religious or political groups.
FAC:         Buildings, airports, highways, bridges, etc.
ORG:         Companies, agencies, institutions, etc.
GPE:         Countries, cities, states.
LOC:         Non-GPE locations, mountain ranges, bodies of water.
PRODUCT:     Objects, vehicles, foods, etc. (Not services.)
EVENT:       Named hurricanes, battles, wars, sports events, etc.
WORK_OF_ART: Titles of books, songs, etc.
LAW:         Named documents made into laws.
LANGUAGE:    Any named language.
DATE:        Absolute or relative dates or periods.
TIME:        Times smaller than a day.
PERCENT:     Percentage, including ”%“.
MONEY:       Monetary values, including unit.
QUANTITY:    Measurements, as of weight or distance.
ORDINAL:     “first”, “second”, etc.
CARDINAL:    Numerals that do not fall under another type.
'''
# import spacy

# nlp = spacy.load("en_core_web_lg")

# text = 'Do you like Pizza?'
# doc = nlp(text)

# #response = 'Hello <HUMAN>, nice to meet you!'

# entities=[(i, i.label_) for i in doc.ents]
# #entities=[(i, i.label_) for i in doc.ents if i.label_ in ['PERSON','ORG','NORP']]
# print(entities)
# print(response.replace("<HUMAN>", str(entities[0][0])))

# import requests
# '''
# Wheather API Test
# '''
# BASE_URL = "https://api.openweathermap.org/data/2.5/weather?id=524901&appid="
# API_KEY = open('data/api_key.txt','r').read()
# CITY = "bdjbsdjbdjs387z3zabdsa"

# url = BASE_URL + API_KEY + "&q=" + CITY + "&units=metric"

# response = requests.get(url).json()
# print(len(response))

# temp = response['main']['temp']
# temp_feels_like = response['main']['feels_like']
# humidity = response['main']['humidity']
# description = response['weather'][0]['description']

# print(f'''General Weather in {CITY}: {description}
# Temperature in {CITY}: {temp}°C
# feels like: {temp_feels_like}°C
# Humidity is: {humidity}%
#       ''')

# '''
# Gedächtnis speichern erste Tests (letzte x Responses speichern)
# '''
# latest_response_memory = []
# latest_response_memory.append("First")
# latest_response_memory.append("Second")
# latest_response_memory.append("Third")
# print(latest_response_memory)
# latest_response_memory.append("Fourth")
# if len(latest_response_memory) > 3:
#     latest_response_memory = list([entry for entry in latest_response_memory if latest_response_memory.index(entry) > 0])
# print(latest_response_memory)
# latest_response_memory.append("Fifth")
# if len(latest_response_memory) > 3:
#     latest_response_memory = list([entry for entry in latest_response_memory if latest_response_memory.index(entry) > 0])
# print(latest_response_memory)

# '''
# do you like/hate xxx
# '''
# import string
# text = "Do you like Pizza or Pasta?"
# response = text.split("like",1)[1]
# print(response)
# response = response.translate(str.maketrans('', '', string.punctuation))
# print(response)


#import spacy


#test Google Suche
# from googleapiclient.discovery import build

# def google_search(search_term):
#     api_key = "AIzaSyAxbO-5Ly0BokLfRJGgAPoLhdG5SM-F_dk" #The API_KEY you acquired
#     cse_id = "f0add6a68738b4d9e" #The search-engine-ID you created
#     service = build("customsearch", "v1", developerKey=api_key)
#     res = service.cse().list(q=search_term, cx=cse_id, num=1).execute()
#     output = ""
#     for result in res['items']:
#         output += result['snippet']
#     print(output+"\n")
#     if output.split()[3] == '...':
#         output = output.lstrip(output.split('...')[0])
#         output = output.lstrip('...')
#     return output


# print(google_search('Facts about France'))



# nlp = spacy.load("en_core_web_lg")

# #text = 'Can you get me some information for tigers in india?'
# text = 'Tell me some information for informatik in java'
# doc = nlp(text)

# sentence_words = []
# for token in doc:
#     sentence_words.append(token.lemma_)
    
# for elem in sentence_words:
#     if "for" == elem:
#         index_of_elem = sentence_words.index(elem)
#         print(elem)
#         print(index_of_elem)
#         splitted_message_topic = list(sentence_words)[index_of_elem+1:]
#         print(splitted_message_topic)
