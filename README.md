# Serenera
Monitor Chrome Browsing to detect levels of Depression 

---

## Overview

Google receives 63000 searches per second on any given day. An average person conducts 3-4 searches every day. According to a report 322 million people worldwide live with depression. Depression is the leading cause of disability worldwide. Almost 75% of people with mental disorders remain untreated in developing countries with almost 1 million people taking their lives each year.

Detecting earlier depression can be a huge step to address the mental illness and offer support to the people suffering from this terrible mental illness.

This depression can be easily detected in the first stages using the pattern seen in search queries. Text analysis, owner analysis (behavior patterns like searches-per-day), temporal analysis (time of day when people search), and visual analysis of pictures searched could be the parameters of detecting depression.

Women experience depression at roughly twice the rate of men. Fewer than half of the women who experience clinical depression will ever seek care. Interactive quizzes and chatbots could help them overcome this depression by providing information about a good doctor.

Thus, our application Serenera aims to reduce depression and instil mental peace and serenity.

![alt text](https://github.com/serenera/Serenera/blob/master/extension/product/ser.png)

---

# Approach:

**UI**
- The user interface is a chrome extension, i.e., a web-based UI.
- When the extension is enabled, it gives the depression levels of the person browsing on a scale of 1 to 10. A rating of 1 would indicate high levels of depression, while a rating of 10 will indicate low levels of depression.
- This add-on additionally suggests measures and therapies to deal with depression. For example, depression relieving music, an appointment with a doctor or psychiatrist, etc.
- There is also therapy chatbot or survey which helps to relieve depression and anxiety of the person. For now, it is just a simple chatbot created from `Landbot.io`. In the upcoming versions, we are planning to make it even more intelligent so as to tend to user needs as efficiently as possible.

**Backend**
- The backend consists of Machine Learning algorithms and AI models to detect/predict depression levels.
- Chrome browsing of the user is monitored. It retrieves data based on google search results of the person.For this purpose, we are working with the browser history of the user. 
- The textual data retrieved from chrome is analyzed using NLP algorithms, and predictions are made on the same

## ML Algorithm in detail

There are two python files for predicting depression. In dep1.py, python code is written  for creating model and save a moel. In the second file dep2.py, it takes saved model from first file and use it for prediction. 

**dep1.py - Creating Model**
- For model creation, NLP is used to extract depressive words by training a classifier to predict a rating (from 1 to 10) based on the text of the search History.
- The dataset `data.csv` contains positive and depressive sentences collected from social media. In the dataset, Label for depressive sentences is “1” and for positive sentences, it is “0”. 
- The data is passed to a classifier which classifies the positive and the depressive sentences.
- It preprocess the data before training. In processing, first it will break the text apart into separate tokens. Sentences are often separated (tokenized) wherever there is a period. 
- After that it removes most obvious non alphanumeric characters, (stop words) and any unnecessary punctuation.
- The Algorithm uses the concept of TF(Term Frequency) and IDF(Inverse Document Frequency). Term Frequency is a count of how many times a word occurs in a given document. The Inverse Document Frequency is the the number of times a word occurs in a corpus of documents. 
- Tf-Idf is used to weight words according to how important they are. Words that are used frequently in many documents will have a lower weighting while infrequent ones will have a higher weighting. Below is the formula:
`w(i,j) = TF(i,j) * log(N / IDF(i))`
 Here, N = total sentences
 - For training it calculates the `tf_idf` score by summing `tf-idf` values and the total is then divided by the summation of all the document `tf-idf` values.
 - This `tf-idf` weighting scheme is used to score sentence’s relevance given a user query.
 - After creating a model, it saved the model in a file for further prediction.
 
 **dep2.py - Prediction based on Model**
 - It loads the model that is created in `dep1.py`
 - Then it takes user’s chrome history as an input text (in csv format) and pass the
each row to the model to predic
- The predict function of model predicts the output on each row. The output is true if the sentence is depressive otherwise the output is false.
- Rating is done based on the number of depressive sentences.  

---

## Dependencies

Make sure you have these installed on your system before running the application

**Prediction using Machine Learning
(dep1.py, dep2.py)**
- `$ sudo apt-get install python3.6`
- `$ sudo apt-get install pip3`
- `$ sudo pip3 install -U nltk`
- `$ sudo pip3 install pandas`
- `$ sudo pip3 install numpy`

**For extracting Chrome History
(browserhistory.py, gethistory.py, setup.py)
Libraries used**
- `import csv`
- `import os`
- `import sqlite3`
- `import sys`
- `from datetime import datetime`
- `import copy`
- `import shutil`

**Connection of Python Backend to Front end:**
- Install Flask
		- `$ sudo pip3 install Flask`
- File structure: app.py
  - Templates(dir) - `index.html`
                   - `response.html`

---

## Running the Application

Extract the compressed zip file `Serenera.tar.xz` or clone this repository.

**Start the backend server**
- Open the terminal
- Type the command
  - `sudo python3 app.py`
- Wait for some time for the server to be completely up and running

**Loading the Chrome Extension**
- Open `Google Chrome` browser
- Click on the 3 dots on top right corner of the browser window
- Choose `More tools > Extensions`
- In the `extensions` browser tab, switch-on the `Developer mode` on the top right side
- Choose `Load unpacked`
- Locate and choose the `extension` folder from extracted file

The extension icon appears. You can navigate through the extension and view its features! 

---

## References and Credits

- https://arxiv.org/pdf/1804.07000.pdf
- https://arxiv.org/pdf/1709.05865.pdf
- HTML Templates
  - Agnes (For music page)
  - Ethereal (For product page)
- Image Credits : Google Images
- Background Music :  Trusted Advertising (By David Renda)

---



