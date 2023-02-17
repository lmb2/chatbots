# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 17:54:58 2022

@author: Laura-Marie Behmenburg und Fabian van Treek
"""

from chatting_hope import get_bot_response

from typing import List

from chatbotsclient.chatbot import Chatbot
from chatbotsclient.message import Message


def get_answer(message, conversation):
    return get_bot_response(message)

def respond(message: Message, conversation: List[Message]):
    answer = get_answer(message.message, conversation)
    return answer


chatbot = Chatbot(respond, "Hope")