# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 12:51:18 2022

@author: Fabian
"""

# import tasks

# method_dir = {
#     "Redirecting to Google...": "do_google_search",
#     "Date and Time": "do_current_date_and_time"
#               }

# #function = globals()[method_dir.get("print")]
# #function()


# function_name = method_dir.get("Date and Time")
# print(eval("tasks."+function_name + "()"))

# print(method_dir.keys())



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
import spacy
#from spacy import displacy

nlp = spacy.load("en_core_web_lg")

text = 'Hello my name is Fabian'
doc = nlp(text)

response = 'Hello <HUMAN>, nice to meet you!'

#entities=[(i, i.label_) for i in doc.ents]
entities=[(i, i.label_) for i in doc.ents if i.label_ in ['PERSON','ORG','NORP']]
print(entities)
#print(response.replace("<HUMAN>", str(entities[0][0])))