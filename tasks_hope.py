# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 13:11:25 2022

@author: Laura-Marie Behmenburg und Fabian van Treek
"""
from datetime import datetime
import requests
import wikipediaapi
from googleapiclient.discovery import build
    
def do_current_date_and_time():
   return datetime.today().strftime('%d-%m-%Y %H:%M:%S')

def do_current_date():
    return datetime.today().strftime('%d-%m-%Y')
    
def do_current_time():
    return datetime.today().strftime('%H:%M:%S')

'''
Wetter mittels API für gewünschten Ort bestimmen und Antwort bauen
'''
def do_weather_in(location,splitted=True):
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

        answer = f'''General Weather in {CITY}: {description}. Temperature in {CITY}: {temp}°C, feels like: {temp_feels_like}°C. Humidity is: {humidity}% '''
    else:
        answer = "Sorry, can't find location."
    return answer

'''
Wikipedia-Suche mittels Wikipedia-API
Ausgabe der ersten 3 Sätze des gefundenen Wikipedia-Artikels
'''
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

'''
Google-Suche mittels Google-API
Ausgabe des ersten Eintrags den die erstelle Google-Suchmaschine findet
'''        
def do_google_search(search_term,splitted=True):
    api_key = open('data/google_api_key.txt','r').read() #The API_KEY you acquired
    cse_id = open('data/google_cse_id.txt','r').read() #The search-engine-ID you created
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, num=1).execute()
    service.close()
    output = ""
    for result in res['items']:
        output += result['snippet']
    if output.split()[3] == '...':
        output = output.lstrip(output.split('...')[0])
        output = output.lstrip('...')
    return output

def run_test():
    print(do_google_search("What is the largest fish?"))
    print(do_weather_in("Düsseldorf"))
    #print(do_wikipedia_search(["Berlin","Cologne"]))

if __name__ == '__main__':
    run_test()