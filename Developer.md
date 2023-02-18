# Developer Information

- [Modules & Functions](#modules--functions)
- [How to modify intents](#modify-intents)
- [How to modify other behavior](#modify-other-behaviors)

## Modules & Functions

- ### <b>training_hope.py</b>

    In this file a Tensorflow-keras model is trained by using the [intents-file](data/intents_hope.json). First each pattern is gonna to be tokenized and lemmatized, this data is set in relation to the respective pattern-tag. While iterating through all patterns there are gonna be two list created. One with all words, duplicates gonna be deleted, and one with all tags(classes). Then bag-of-words(bow) are created for each tokenized and lemmatized pattern. The bow and the respective tag(class) of the created bow are the data which are given to the model to train.


- ### <b>chatting_hope.py</b>

    This is the main-file of the bot. The created model will be used to predict the pattern-tag based on the user-input. The bot then either knows which response to pick or what task to be executed. Some other behavior will be explained [here](#modify-other-behaviors). <br>
    Functions short explained:
    - <b>clean_up_sentence(sentence)</b>: tokenizing and lemmatizing the user-input
    - <b>bag_of_words(sentence)</b>: create a bag-of-words from the user-input
    - <b>content_pattern_check(predicted_class, sentence)</b>: checks wether the patterns of the predicted tag(class) is content correct to the user-input 
    - <b>predict_class(sentence)</b>: predicts the possible tags(classes) that come into question for the response by using the trained model
    - <b>get_information(tag, message)</b>: filters information out of the user-input for further usage
    - <b>safe_in_memory(tag, response)</b>: safes the tag and response of the latest bot-answer into the memory
    - <b>get_last_memory_tag()</b>: get the last memory 
    - <b>get_last_but_one_memory_tag()</b>: get the last but one memory
    - <b>get_response(message)</b>: main-method for final response generation, task calling and other behavior
    - <b>run_hope()</b>: method to run the bot 
    - <b>get_bot_response(user_input)</b>: method for the interaction with other bots, used in the [chatbot_moderator_interaktion.py](#chatbot_moderator_interaktionpy)
    <p>


- ### <b>tasks_hope.py</b>

    This file contains all the implemented tasks that the bot can do. These are called and used from the main-file.<br>
    Implemented task-functions short explained:
    - <b>do_current_date_and_time()</b>: returns the current date and time
    - <b>do_current_date()</b>: returns the current date
    - <b>do_current_time()</b>: returns the current time
    - <b>do_weather_in(location, splitted=True)</b>: returns the weather at given location 
    - <b>do_wikipedia_search(possibleTopics, splitted=True)</b>: returns the first sentences of a wikipedia-article by given topic
    - <b>do_google_search(search_term, splitted=True)</b>: returns the first output found by google the given term
    <p>


- ### <b>chatbot_moderator_interaktion.py</b>

    Here you can let the bot interact with other chatbots. For this you have to follow the intructions of the [chatbotsclient](https://github.com/Robstei/chatbotsclient). When done, you just execute the file by using: 
    ```
    python chatbot_moderator_interaction.py
    ```

## Modify intents

To add,change or delete parts of the intents you need to unterstand the structure. Each intent is seperated in a <b>tag(class)</b> that describes the content in a simple way, a <b>list of patterns</b> which are the trigger for the bot and a <b>list of responses</b> from which the bot will pick a response. <br>
An example:
```json
    {
        "tag": "courtesyGreeting",
        "patterns": [
              "How are you?",
              "Hi how are you?",
              "Hello how are you?",
              "Hola how are you?",
              "Hope you are doing well?",
              "Hello hope you are doing well?"
        ],
        "responses": [
              "Hello, I am great, how are you?",
              "Hello, how are you? I am great thanks!",
              "Hello, I am good thank you, how are you?",
              "Hi, I am great, how are you?",
              "Hi, how are you? I am great thanks!",
              "Hi, I am good thank you, how are you?",
              "Hi, good thank you, how are you?"
        ]
    }
```

## Modify other behaviors

Other behaviors are defined by dictionaries or lists that determine when it triggers and what do do in the situation. These are:
- [Get information from user-input](#get-information)
- [Execute tasks due to user-input](#execute-tasks)
- [Direct responses based on prior response](#direct-responses)
- [Direct task with user-input based on prior response](#direct-task-with-input)
- spacy_content_check

In the following all these parts are gonna be explained, that you know how to modify them or add your own entries.

- ### <b>Get information</b>
    This shows you multiple ways to get information out of the user-input. Using a dictionary filled with the parameters needed.<br>
    The dictionary with the required information looks like this:
    ```
    get_information_dict = {
        "courtesyGreetingResponse": (["<HUMAN>",""],["PERSON","ORG","NORP"]),
        "weather": (["<>",""],["PERSON","ORG","GPE","EVENT"]),
        "wikipediaSearch": (["<>","split"],["about","for"]),
        "google": (["<>","pure"],[""])
    }
    ```
    The basic pattern is: `` "Tag": ([parameter_name_to_change,splitTrigger],[entity_names_to_check_for]) `` <br>
    <br/>
    <ins>Let's look at the first dictionary entry:</ins> <br>
    This is gonna get triggered when the bot determines ``"courtesyGreetingResponse"`` as tag(class) to chose a response from. <br>
    When it's triggered the bot knows that he has to check the user-input by using the spacy-entity-check with the given parameters ``["PERSON","ORG","NORP"]``, because there is no <b>splitTrigger</b> defined. <br>
    Afterwards the bot replaces the obtained information with the given part that should be replaced: ``["<HUMAN>",""]``. <br>
    The intent part of this example looks like this:
    ```json
    {
        "tag": "courtesyGreetingResponse",
        "patterns": [
              "Good thanks! My name is Adam",
              "Good thanks. This is Adam",
              "Good thanks. I am Adam",
              "Im fine, thanks. My name is Adam",
              "Great thanks! My name is Bella",
              "Great thanks. I am Bella",
              "My name is Adam",
              "My name is Bella",
              "I am Bella",
              "I am Adam. Nice to meet you."
        ],
        "responses": [
            "Great! Hi <HUMAN>! How can I help?",
            "Good! Hi <HUMAN>, how can I help you?",
            "Cool! Hello <HUMAN>, what can I do for you?",
            "OK! Hola <HUMAN>, how can I help you?",
            "OK! hi <HUMAN>, what can I do for you?"
        ]
    }
    ```
    <br/><br/>
    <ins>Let's take a look at the second entry:</ins> <br>
    This get's triggered when the bots determines ``"weather"`` as tag(class) to chose a response from. <br>
    When it's triggered the bot knows that he has to check the user-input by using the spacy-entity-check with the given parameters ``["PERSON","ORG","GPE","EVENT"]``, because there is no <b>splitTrigger</b> defined. <br>
    Afterwards the bot uses the obtained information for the next steps. <br>
    The intent part of this example looks like this:
    ```json
    {
        "tag": "weather",
        "patterns": [
            "how is the temperature in Düsseldorf",
            "how is the weather in Köln",
            "how hot is it in Aachen"
        ],
        "responses": [
            "Weather"
        ]
    }
    ```
    <br/><br/>
    <ins>Let's take a look at the third entry:</ins> <br>
    This get's triggered when the bots determines ``"wikipediaSearch"`` as tag(class) to chose a response from. <br>
    When it's triggered the bot knows that he has to split the user-input appointed by ``["<>","split"]`` and to split at the given words ``["about","for"]``. <br>
    Afterwards the bot uses the obtained information for the next steps. <br>
    The intent part of this example looks like this:
    ```json
    {
        "tag": "wikipediaSearch",
        "patterns": [
            "can you tell me something about apples",
            "do you know something about cars",
            "get me some information for",
            "get me some informaton about"
        ],
        "responses": [
            "WikiSearch"
        ]
    }
    ```
    <br/><br/>
    <ins>Let's take a look at the last entry:</ins><br>
    This get's triggered when the bot determines ``"google"`` as tag(class) to chose a response from. <br>
    Settled by the ``["<>","pure"]`` the bot knows that he has to use the complete user-input for the next step. <br>
    The intent part of this example looks like this:
    ```json
    {
        "tag": "google",
        "patterns": [],
        "responses": [
            "Redirecting to Google..."
        ]
    }
    ```
    <br/><br/>
- ### <b>Execute tasks</b>
    The following shows how to add tasks and their triggers, so the bot can execute them in the way you want to.<br>
    The dictionary with the required information looks like this:
    ```
    task_dict = {
        "Redirecting to Google...": "do_google_search",
        "Date and Time": "do_current_date_and_time",
        "Date": "do_current_date",
        "Time": "do_current_time",
        "Weather": "do_weather_in",
        "WikiSearch": "do_wikipedia_search"
    }
    ```
    The basic pattern is: `` "Response": "function_name" `` <br>
    <br/>
    <ins>Let's look at the first dictionary entry to giving you an example:</ins> <br>
    The task gets triggered when the determined response the bot has chosen is equal to ``"Redirecting to Google..."``. <br>
    Then the task named by their method-name in the [tasks_hope.py](#tasks_hopepy), in this case ``"do_google_search"`` is gonna be executed.<br>
    <br/>
    The other entries are working the same way. In case a function needs parameters to work, obtained from the user-input, that handling take place in the [get information](#get-information) part. <br>
    Implemented and shown examples are <b>weather, wikipediaSearch and google</b>.
    <br/><br/><br/>

- ### <b>Direct responses</b>
    This part is all about handling behavior in case a specific response has been send last and the user replied something that should be handled in a different way.<br>
    The dictionary with the required information looks like this:
    ```
    direct_response_dict = {
        "wrongAnswer": ("wrongAnswerResponse",["wikipediaSearch"]),
        "anotherJoke": ("jokes",["jokes"])
    }
    ```
    The basic pattern is: ``"Tag": (newResponseTag,[latestMemoryTagsTriggers])`` <br>
    <br/>
    <ins>Let's look at the first dictionary entry:</ins> <br>
    In case the determined tag(class) the bot has predicted is ``"wrongAnswer"``, the bot is gonna to check if the last entry in his memory is ``["wikipediaSearch"]``.<br>
    If thats true, the bot sets ``"wrongAnswerResponse"`` as new tag(class) to chose a response from.<br>
    If not, the previous determined tag(class) stays and the bot choses the response from there.<br>
    The dictionaries with the required information looks like this:
    <table>
    <tr>
    <th>predicted tag(class)</th>
    <th>direct response tag(class)</th>
    </tr>
    <tr>
    <td>

    ```json
    {
        "tag": "wrongAnswer",
        "patterns": [
            "That was not the answer i was looking for.",
            "Thats not the topic i wanted."
        ],
        "responses": [
            "I am sorry. Is there anything else i can help you with?"
        ]
    }
    ```
    </td>
    <td>

    ```json
    {
        "tag": "wrongAnswerResponse",
        "patterns": [],
        "responses": [
            "I am sorry. What topic are you looking for?"
        ]
    }
    ```

    </td>
    </tr>

    </table>

    <br/>

    <ins>Let's take a look at the second entry:</ins> <br>
    In case the determined tag(class) the bot has predicted is ``"anotherJoke"``, the bot is gonna to check if the last entry in his memory is ``["jokes"]``.<br>
    If thats true, the bot sets ``"jokes"`` as new tag(class) to chose a response from.<br>
    If not, the previous determined tag(class) stays and the bot choses the response from there.<br>
    The dictionaries with the required information looks like this:
    <table>
    <tr>
    <th>predicted tag(class)</th>
    <th>direct response tag(class)</th>
    </tr>
    <tr>
    <td>

    ```json
    {
        "tag": "anotherJoke",
        "patterns": [
            "get me more",
            "tell me another one",
            "more jokes"
        ],
        "responses": [
            "That was no Joke!"
        ]
    }
    ```
    </td>
    <td>

    ```json
    {
        "tag": "jokes",
        "patterns": [
            "Tell me a joke",
            "Joke",
            "Make me laugh",
            "Can you be a bit funny",
            "Tell me something funny!",
            "Do you know a joke?",
            "How about a joke",
            "Do you know any jokes?",
            "Any joke for me?",
            "Give me a joke"
        ],
        "responses": [
            "A perfectionist walked into a bar...apparently, the bar wasn't set high enough",
            "I ate a clock yesterday, it was very time-consuming"
        ]
    }
    ```
    <b>* the jokes-respones are way more extensive, shortened here</b>
    </td>
    </tr>

    </table>

    <br/>

- ### <b>Direct task with input</b>
    Test