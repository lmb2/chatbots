# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 17:54:58 2022

@author: Fabian
"""

from chatbot_intents_methods import get_bot_response

while True:
    userInput = input("TestInput:")    
    print(get_bot_response(userInput))
