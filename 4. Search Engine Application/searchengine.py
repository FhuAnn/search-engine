from flask import Flask,render_template, request
import pickle 
from sklearn.feature_extraction.text import TfidfVectorizer
import networkx as nx 
import json
import numpy as np

app = Flask(__name__,template_folder="./static/")

@app.route("/")
def websearch(): 
    return render_template("websearch.html")

@app.route("/imagesearch")
def imagesearch():
    return render_template("imagesearch.html")

@app.route("/a")
def a():
    return render_template("A.html")

@app.route("/b")
def b():
    return render_template("B.html")

@app.route("/c")
def c():
    return render_template("C.html")

@app.route("/d")
def d():
    return render_template("D.html")

@app.route("/e")
def e():
    return render_template("E.html")

@app.route("/websearch",methods = ["GET","POST"])
def web_search():
    if request.method=="POST":
        query = request.form["query"]
        if query=="":
            return render_template("websearch.html")
    websites= [
            'http://localhost:5000/a',
            'http://localhost:5000/b',
            'http://localhost:5000/c',
            'http://localhost:5000/d',
            'http://localhost:5000/e']
    tokenized_text = load_tokenized_text("tokenized_text_pickle.pkl")
    tfidf = TfidfVectorizer()
    tfidf_vectors = tfidf.fit_transform

    return render_template("result.html",data = query)

@app.route("/search_images", methods=["GET","POST"])
def search_images():
    if request.method == "POST":
        query = request.form["query"].lower()
        if query == "":
            return render_template("imagesearch.html")
        
        with open("images.json","r") as f :
            images = json.load(f)
        print(images,"jkjkjdfkj")
        #Search for images with alt text and tittle trhat contain the query term
        results = []
        for img in images:
            if query in img["alt_text"] or query in img["title"]:
                results.append(img)
            else:
                continue
        
        if len(results) == 0:
            return render_template("notfound.html")

        return render_template("imageresults.html",data = [results,query])

@app.route("/reverseimagesearchresult",methods=["GET","POST"])
def reverseimagesearchresult():
    if request.method == "POST":
        file = request.files["query_img"]


def load_tokenized_text(filename):
    tokenized_text = pickle.load(open(filename,"rb"))
    return tokenized_text

if __name__ == "__main__":
    app.run(debug=True)