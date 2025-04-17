from pymongo import MongoClient
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from nltk.stem import PorterStemmer

conn = "mongodb://localhost:27100,localhost:27200"
client = MongoClient(conn)
db = client["search_engine"]

# Collections
documents_collection = db["documents"]
inverted_index_plain_collection = db["inverted_index_plain"]
inverted_index_shard_collection = db["inverted_index_shard"]


# nltk.download('punkt')
# nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

def build_inverted_index_plain():
    inverted_index = defaultdict(lambda: defaultdict(int))

    # Lặp qua tất cả các tài liệu trong collection 'documents'
    for doc in documents_collection.find():
        doc_id = doc['_id']
        text = f"{doc['title']} {doc['body']}"

        # Tokenize và làm sạch
        tokens = word_tokenize(text.lower())
        filtered_tokens = [
            stemmer.stem(word) for word in tokens 
            if word.isalnum() and word not in stop_words
        ]

        # Cập nhật inverted index với tần suất
        for word in filtered_tokens:
            inverted_index[word][doc_id] += 1
            
    # Lưu inverted index vào collection 'inverted_index'
    for word, doc_freq in inverted_index.items():
        inverted_index_plain_collection.update_one(
            {"word": word},
            {"$set": {"documents": dict(doc_freq)}},  # Lưu tần suất từ theo doc_id
            upsert=True
        )
       
       
def get_shard_word(word):
    first_char = word[0]
    if 'a' <= first_char <= 'g':
        return 'a'
    elif 'h' <= first_char <= 'n':
        return 'h'
    elif 'o' <= first_char <= 'u':
        return 'o'
    else:
        return 'remains'
        
def build_inverted_index_sharding():
    inverted_index = defaultdict(lambda: defaultdict(int))

    # Lặp qua tất cả các tài liệu trong collection 'documents'
    for doc in documents_collection.find():
        doc_id = doc['_id']
        text = f"{doc['title']} {doc['body']}"

        # Tokenize và làm sạch
        tokens = word_tokenize(text.lower())
        filtered_tokens = [
            stemmer.stem(word) for word in tokens 
            if word.isalnum() and word not in stop_words
        ]

        # Cập nhật inverted index với tần suất
        for word in filtered_tokens:
            inverted_index[word][doc_id] += 1
            
    # Lưu inverted index vào collection 'inverted_index'
    for word, doc_freq in inverted_index.items():
        shard_key = get_shard_word(word)
        inverted_index_shard_collection.update_one(
            {"word": word, "shard_word": shard_key},  
            {
                "$set": {
                    "documents": dict(doc_freq),
                    "shard_word": shard_key
                }
            },
            upsert=True
        )
        
# build_inverted_index_sharding()
build_inverted_index_plain()