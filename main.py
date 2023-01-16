# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 17:54:58 2022

@author: Fabian
"""

from chatbot_intents_methods import get_bot_response

import random
from typing import List



from chatbotsclient.chatbot import Chatbot
from chatbotsclient.message import Message


def random_answer(message, conversation):
    return get_bot_response(message)


def respond(message: Message, conversation: List[Message]):
    # custom answer computation of your chatbot
    answer = random_answer(message.message, conversation)
    return answer


chatbot = Chatbot(respond, "Hope")
