from pymongo import MongoClient
from faker import Faker
import uuid

conn = "mongodb://localhost:27100,localhost:27200"
client = MongoClient(conn)
db = client["search_engine"]
documents = db["documents"]
faker = Faker()

def tokenize(text):
    return [word.lower() for word in text.split() if word.isalpha()]

def seeding(docs_num=10000):
    for _ in range(docs_num):
        _id = str(uuid.uuid4())
        title = faker.sentence()
        body = faker.paragraph(nb_sentences=5)
        full_text = title + " " + body
        documents.insert_one({
            "_id": _id,
            "title": title,
            "body": body,
        })
        
seeding(10_000)