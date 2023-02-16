# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 10:49:47 2022

@author: Laura-Marie Behmenburg und Fabian van Treek
"""
import random
import json
import pickle
import numpy as np
import spacy

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD

nlp = spacy.load("en_core_web_lg")

intents = json.loads(open('data/intents_hope.json',encoding='utf8').read())

words = []
classes = []
documents = []
ignore_letters = ['?', '!', '.', ',']


'''
Alle intents durchgehen
tokenzize und lemmatize anwenden -> in words speichern als einzelne lists
und in documents werden die paare zu den tag gespeichert -> z.B. (['how', 'is', 'it', 'going'], 'greetings')
'''
for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list= []
        spacy_doc = nlp(pattern)
        for token in spacy_doc:
            if token.lemma_ not in ignore_letters:
                word_list.append(token.lemma_)
            
        words.extend(word_list)
        documents.append((word_list, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

'''
alle Duplikate entfernen (set entfernt Duplikate) und Sortieren (sorted)
'''
words = sorted(set(words))
classes = sorted(set(classes))

'''
Erstellte Listen mit den lemmatized und tokenized Words
und Klassen speichern
'''
pickle.dump(words, open('data/words_intents.pkl', 'wb'))
pickle.dump(classes, open('data/classes_intents.pkl', 'wb'))

'''
Bag of words erstellen
setzen von word value auf 1 oder 0, je nachdem ob sie im pattern vorkommen oder nicht
'''
training = []
output_empty = [0] * len(classes)
for document in documents:
    bag = []
    word_patterns = document[0]
    for word in words:
        if word in word_patterns:
            bag.append(1)
        else:
            bag.append(0)
            
    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    '''
    hier hat man dann von jeweiligen Pattern den Word-Bag vom abgleich aller vorkommenden Wörter 
    und der jeweiligen Klasse(Tag) aus welcher das Pattern war = 1 in der output_row
    '''
    training.append([bag, output_row])

'''
Training daten mischen und in np array speichern
und trennen der Daten in x und y -> x = bag-Daten und y = output_row-Daten (Klassen/Tags)
'''
random.shuffle(training)
training = np.array(training)

train_x = list(training[:, 0])
train_y = list(training[:, 1])
 
'''
Model mit zuvor generierten Trainingsdaten erstellen und speichern
'''
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

sgd = SGD(lr=0.01, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size= 5, verbose=1)
model.save('data/chatbotmodelintents.h5', hist)