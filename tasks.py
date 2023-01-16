# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 13:11:25 2022

@author: Fabian
"""
from datetime import datetime
import requests
import wikipediaapi
from googleapiclient.discovery import build

def do_google_search():
    return "Doing search..."
    
def do_current_date_and_time():
   return datetime.today().strftime('%d-%m-%Y %H:%M:%S')

def do_current_date():
    return datetime.today().strftime('%d-%m-%Y')
    
def do_current_time():
    return datetime.today().strftime('%H:%M:%S')

def do_weather_in(location):
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?id=524901&appid="
    API_KEY = open('data/api_key.txt','r').read()
    CITY = str(location).title()

    url = BASE_URL + API_KEY + "&q=" + CITY + "&units=metric"

    response = requests.get(url).json()
    if len(response) > 3:
        temp = response['main']['temp']
        temp_feels_like = response['main']['feels_like']
        humidity = response['main']['humidity']
        description = response['weather'][0]['description']

        answer = f'''General Weather in {CITY}: {description}
        Temperature in {CITY}: {temp}°C
        feels like: {temp_feels_like}°C
        Humidity is: {humidity}% '''
    else:
        answer = "Sorry, can't find location."
    return answer
    
def do_wikipedia_search(possibleTopics,splitted=True):
    wiki_wiki = wikipediaapi.Wikipedia('en')
    if splitted:
        for topic in possibleTopics:
            wiki_page = wiki_wiki.page(topic)
            if(wiki_page.exists()):
                return wiki_wiki.extracts(wiki_page, exsentences=3)
            else:
                return "Sorry, i didn't find anything to your question"
    else:
        wiki_page = wiki_wiki.page(possibleTopics)
        if(wiki_page.exists()):
            return wiki_wiki.extracts(wiki_page, exsentences=3)
        else:
            return "Sorry, i didn't find anything to your question"
        
def do_google_search(search_term):
    api_key = open('data/google_api_key.txt','r').read() #The API_KEY you acquired
    cse_id = open('data/google_cse_id.txt','r').read() #The search-engine-ID you created
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, num=1).execute()
    output = ""
    for result in res['items']:
        output += result['snippet']
    return output

def run_test():
    print(do_google_search("What is the largest fish?"))
    print(do_weather_in("Düsseldorf"))
    #print(do_wikipedia_search(["Berlin","Cologne"]))

if __name__ == '__main__':
    run_test()