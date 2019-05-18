# -*- coding: utf-8 -*-
"""
Created on Wed May 15 22:04:22 2019

@author: POOJA
"""
#import nltk
#nltk.download('punkt')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import pickle
from math import log
import csv
import io
import gethistory

def process_text(text, lower_case = True, stem = True, stop_words = True, gram = 2):
    if lower_case:
        text = text.lower()
    words = word_tokenize(text)
    words = [w for w in words if len(w) > 2]
    if gram > 1:
        w = []
        for i in range(len(words) - gram + 1):
            w += [' '.join(words[i:i + gram])]
        return w
    if stop_words:
        sw = stopwords.words('english')
        words = [word for word in words if word not in sw]
    if stem:
        stemmer = PorterStemmer()
        words = [stemmer.stem(word) for word in words]   
    return words


class Classifier(object):
    def __init__(self, trainData):
        self.text, self.labels = trainData['text'], trainData['label']

    def train(self):
        self.calc_TF_and_IDF()
        self.calc_TF_IDF()

    def calc_TF_and_IDF(self):
        noOftext = self.text.shape[0]
        self.depressive_text, self.positive_text = self.labels.value_counts()[1], self.labels.value_counts()[0]
        self.total_text = self.depressive_text + self.positive_text
        self.depressive_words = 0
        self.positive_words = 0
        self.tf_depressive = dict()
        self.tf_positive = dict()
        self.idf_depressive = dict()
        self.idf_positive = dict()
        for i in range(noOftext):
            text_processed = process_text(self.text.iloc[i])
            count = list()
            for word in text_processed:
                if self.labels.iloc[i]:
                    self.tf_depressive[word] = self.tf_depressive.get(word, 0) + 1
                    self.depressive_words += 1
                else:
                    self.tf_positive[word] = self.tf_positive.get(word, 0) + 1
                    self.positive_words += 1
                if word not in count:
                    count += [word]
            for word in count:
                if self.labels.iloc[i]:
                    self.idf_depressive[word] = self.idf_depressive.get(word, 0) + 1
                else:
                    self.idf_positive[word] = self.idf_positive.get(word, 0) + 1

    def calc_TF_IDF(self):
        self.prob_depressive = dict()
        self.prob_positive = dict()
        self.sum_tf_idf_depressive = 0
        self.sum_tf_idf_positive = 0
        for word in self.tf_depressive:
            self.prob_depressive[word] = (self.tf_depressive[word]) * log((self.depressive_text + self.positive_text) \
                                                          / (self.idf_depressive[word] + self.idf_positive.get(word, 0)))
            self.sum_tf_idf_depressive += self.prob_depressive[word]
        for word in self.tf_depressive:
            self.prob_depressive[word] = (self.prob_depressive[word] + 1) / (self.sum_tf_idf_depressive + len(list(self.prob_depressive.keys())))
            
        for word in self.tf_positive:
            self.prob_positive[word] = (self.tf_positive[word]) * log((self.depressive_text + self.positive_text) \
                                                          / (self.idf_depressive.get(word, 0) + self.idf_positive[word]))
            self.sum_tf_idf_positive += self.prob_positive[word]
        for word in self.tf_positive:
            self.prob_positive[word] = (self.prob_positive[word] + 1) / (self.sum_tf_idf_positive + len(list(self.prob_positive.keys())))
            
    
        self.prob_depressive_text, self.prob_positive_text = self.depressive_text / self.total_text, self.positive_text / self.total_text
                    
    def classify(self, processed_text):
        pDepressive, pPositive = 0, 0
        for word in processed_text:                
            if word in self.prob_depressive:
                pDepressive += log(self.prob_depressive[word])
            else:
                pDepressive -= log(self.sum_tf_idf_depressive + len(list(self.prob_depressive.keys())))
            if word in self.prob_positive:
                pPositive += log(self.prob_positive[word])
            else:
                pPositive -= log(self.sum_tf_idf_positive + len(list(self.prob_positive.keys()))) 
            pDepressive += log(self.prob_depressive_text)
            pPositive += log(self.prob_positive_text)
        return pDepressive >= pPositive
    
    def predict(self, testData):
        result = dict()
        for (i, text) in enumerate(testData):
            processed_text = process_text(text)
            result[i] = int(self.classify(processed_text))
        return result

Model = pickle.load(open("finalized_model.sav", 'rb'))

with io.open("chrome_history.csv", 'r',encoding="utf8") as csvinput:
    with io.open("history_prediction.csv", 'w',encoding="utf8") as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        reader = csv.reader(csvinput)

        all = []
        true = 0
        false = 0
        for row in reader:
            text = process_text(row[1])
            result= Model.classify(text)
            if result:
                 true = true + 1
            else  :
                false = false + 1
            row.append(result)
            all.append(row)
        print("total depressive sentences : " , true)
        print("total positive sentences : ",false)
        writer.writerows(all)
    #myList = [true, false]
        if (true>=180):
          rate=1
        elif(true>=160):
          rate=2
        elif(true>=140):
          rate=3
        elif(true>=120):
          rate=4
        elif(true>=100):
          rate=5
        elif(true>=80):
          rate=6
        elif(true>=60):
          rate=7
        elif(true>=40):
          rate=8
        elif(true>=20):
          rate=9
        else :
          rate=10
        f= open("extension/try","w+")
        f.write("Depression Rating : ")
        f.write(str(rate))
        f.close()
        f= open("extension/p","w+")
        f.write(str(true))
        f.close()
    csvoutput.close()
csvinput.close()
