#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 13:50:02 2023

@author: Laura
"""

import random
from typing import List

from chatbotsclient.chatbot import Chatbot
from chatbotsclient.message import Message


def random_answer(message, conversation):
    return random.choice(
        [
            "I like zucchini.",
            "I love butter.",
            "I prefer müsli.",
            "Avocados are my favorite.",
        ]
    )


def respond(message: Message, conversation: List[Message]):
    # custom answer computation of your chatbot
    answer = random_answer(message.message, conversation)
    return answer


chatbot = Chatbot(respond, "Chatbot 1")