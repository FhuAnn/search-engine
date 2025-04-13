from flask import Flask, request,render_template
import sqlite3

app = Flask(__name__,template_folder="./static")

@app.route("/")
def home(): 
    return render_template("websearch.html")

@app.route("/websearch",methods=["GET","POST"])
def search():
    #get the query from request
    query = request.form["query"]
    if query == "":
        render_template("websearch.html")

    #Connect to the sqlite database
    conn = sqlite3.connect("crawled_pages.db")
    cursor = conn.cursor()

    #search for websites that match the query in thier cleaned_content
    cursor.execute("SELECT url,title FROM pages WHERE cleaned_content LIKE ? ORDER BY pagerank DESC",('%'+query+'%',))
    urls = cursor.fetchall()
    
    #close the connection
    conn.close()

    #Render the URLs that match the query
    return render_template("results.html",urls=urls, query=query)


if __name__ =="__main__":
    app.run(debug=True)