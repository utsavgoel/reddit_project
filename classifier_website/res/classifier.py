# This file is same as classifier.ipynb

# pip install praw scikit-learn pandas requests
import requests
import json
import pandas as pd
import datetime as dt
import numpy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
import joblib 

def build_classifier():

    data = pd.read_csv('scraped_reddit.csv')

    X = data["title"]
    y = data["flair"]
    #Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    #z_train, z_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    text_clf = Pipeline([('vect', CountVectorizer(token_pattern=r'\b[^\d\W]+\b')),
                    ('tfidf', TfidfTransformer()),
					('clf-svm', SGDClassifier(loss='hinge', penalty='l2',
                        alpha=1e-3, random_state=42)),
    ])
    text_clf = text_clf.fit(X_train.values.astype('U'), y_train.values.astype('U'))

    #Save the model
    joblib.dump(text_clf, 'text_clf.pkl') 
    #predicted = text_clf.predict(X_test.values.astype('U'))
    #print(numpy.mean(predicted == y_test.values.astype('U')))
    #print(predicted)	

def calculate_flare(input):
    topics_dict = { "title":[], 
                "score":[], 
                "id":[], "url":[],  
                "comms_num": [], 
                "created": [], 
                "body":[],
                "flair":[]}
    url = "https://api.pushshift.io/reddit/search/submission/?url=" + input
    json = requests.get(url, headers={'User-Agent': "utsavgoel"})
    json_data = json.json()
    #print(json_data['data'][0])
    if 'data' not in json_data or len(json_data['data']) == 0:
        print("No Data Fetched")
        return
    object = json_data['data'][0]
    if 'link_flair_text' in object:
        topics_dict["title"].append(object['title'])
        topics_dict["score"].append(object['score'])
        topics_dict["id"].append(object['id'])
        topics_dict["url"].append(object['url'])
        topics_dict["comms_num"].append(object['num_comments'])
        topics_dict["created"].append(object['created_utc'])
        topics_dict["body"].append(object['selftext'])
        topics_dict["flair"].append(object['link_flair_text']) 
    else:
        print("No flair in the Reddit Object")
          
    text_clf = joblib.load('classifier_website/res/text_clf.pkl')  
    predicted = text_clf.predict(topics_dict["title"])
    print(predicted)
    return {'url':input, 'flare':predicted[0]}

def testing(str):
    data = []
    for i in range(len(str)):
        str[i] = str[i].strip('\r')
        data.append(calculate_flare(str[i]))
    
    with open('data.json', 'w') as fout:
        json.dump(data, fout)
    return data			

if __name__ == "__main__":
     
    # For testing purpose	
    #build_classifier()
    #testing("abc.txt")  
    input = "https://www.reddit.com/r/india/comments/g1zi21/coronavirus_covid19_megathread_news_and_updates_4/"
    calculate_flare(input)
