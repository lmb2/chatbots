# Tensorflow intent-based Chatbot - Hope

Authors: Laura-Marie Behmenburg, Fabian van Treek
## Installation
Hier muss der Kram mit der File rein, auch wie man ein Conda umgebung anlegt? Das Python installiert sein muss, sollte ja doch klar sein.
### Requirements
Python Conda, ich weiß gerade nicht was noch und welche Versionen oder egal
## Data
The Chatbot Data, based largely on the file _intents_hope.json_ this file, was merged by hand, by some datasets found on the Internet. In addition, further content was added or changed manually.
- [Recognition-dataset from Kaggle](https://www.kaggle.com/datasets/elvinagammed/chatbots-intent-recognition-dataset/code)
- [intents-for-first-aid-recommendations from Kaggle](https://www.kaggle.com/datasets/therealsampat/intents-for-first-aid-recommendations)
- [mental-health-conversational-data from Kaggle](https://www.kaggle.com/datasets/elvis23/mental-health-conversational-data)
- [Intens from Kaggle](https://www.kaggle.com/datasets/chachiawacef/intents)





## Usage
### Train the Bot
Start the following file to start the training:

```
training_hope.py
```
Training must be done once, but if some changes happen to the _intents_hope.json_, by adding new Patterns or changing them. The Bot must be trained again, otherwise the bot does not take over the new changes.
### Start the Bot
Start the following file to start the Bot:

```
chatting_hope.py
```
After starting the Bot the Console should look like this:
```
Bot is running!
Me:
```
Now the Bot is running, and a question or anything else can be written, and the Bot will answer.




