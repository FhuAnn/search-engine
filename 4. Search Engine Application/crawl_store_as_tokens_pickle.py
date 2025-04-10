import pickle
import os
from bs4 import BeautifulSoup
import requests

def save_tokenized_text(tokenized_text,filename):
    with open(filename,"wb") as f:
        pickle.dump(tokenized_text,f)

if not os.path.exists("tokenized_text_pickle.pkl"):
    websites= [
            'http://localhost:5000/a',
            'http://localhost:5000/b',
            'http://localhost:5000/c',
            'http://localhost:5000/d',
            'http://localhost:5000/e']

    text_content=[]

    for website in websites:
        response = requests.get(website)
        soup = BeautifulSoup(response.text,"html.parser")
        text_content.append(soup.get_text())

    stop_words =["the","is","and","to","hi","my","name","a","in","that","for","it","click","here","go"]

    tokenized_text=[]
    for content in text_content:
        tokens = content.lower().split()
        tokenized_text.append([token for token in tokens if token not in stop_words])

    save_tokenized_text(tokenized_text,"tokenized_text_pickle.pkl")