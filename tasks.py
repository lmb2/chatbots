# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 13:11:25 2022

@author: Fabian
"""
from datetime import datetime

def do_google_search():
    return "Doing search..."
    
def do_current_date_and_time():
   return datetime.today().strftime('%d-%m-%Y %H:%M:%S')

def do_current_date():
    return datetime.today().strftime('%d-%m-%Y')
    
def do_current_time():
    return datetime.today().strftime('%H:%M:%S')
