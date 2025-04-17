from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from nltk.stem import PorterStemmer

# Kết nối tới MongoDB
conn = "mongodb://localhost:27100,localhost:27200"
client = MongoClient(conn)
db = client["search_engine"]

# Collections
documents_collection = db["documents"]
inverted_index_plain_collection = db["inverted_index_plain"]
inverted_index_shard_collection = db["inverted_index_shard"]

# Tải bộ stopwords từ NLTK
# nltk.download('punkt')
# nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

# Hàm tìm kiếm sử dụng inverted index trước khi tính toán TF-IDF
def search_plain(query):
    # Tokenize câu truy vấn
    query_tokens = word_tokenize(query.lower())
    filtered_query = [stemmer.stem(word) for word in query_tokens if word.isalnum() and word not in stop_words]

    # Bước 1: Tra cứu inverted index để lấy các tài liệu có liên quan
    relevant_docs = set()

    for word in filtered_query:
        inverted_doc = inverted_index_plain_collection.find_one({"word": word})
        if inverted_doc:
            relevant_docs.update(inverted_doc['documents'].keys())  # Lấy danh sách tài liệu liên quan

    if not relevant_docs:
        return []  # Nếu không có tài liệu nào liên quan

    # Bước 2: Lấy nội dung của các tài liệu liên quan từ MongoDB
    docs = list(documents_collection.find({"_id": {"$in": list(relevant_docs)}}))

    # Lấy văn bản từ các tài liệu
    texts = [doc['title'] + " " + doc['body'] for doc in docs]
    doc_ids = [doc['_id'] for doc in docs]

    tfidf_vectorizer = TfidfVectorizer(stop_words=list(stop_words))
    tfidf_matrix = tfidf_vectorizer.fit_transform(texts)

    # Tính TF-IDF cho câu truy vấn
    query_tfidf = tfidf_vectorizer.transform([query])

    # Tính độ tương đồng giữa câu truy vấn và các tài liệu
    cosine_similarities = (tfidf_matrix * query_tfidf.T).toarray().flatten()

    # Lấy các tài liệu có độ tương đồng cao nhất
    result_docs = []
    for i, score in enumerate(cosine_similarities):
        if score > 0:  # Lọc những tài liệu không có sự tương đồng với truy vấn
            result_docs.append({
                "doc_id": doc_ids[i],
                "title": docs[i]['title'],
                "body": docs[i]['body'],
                "score": score
            })

    # Sắp xếp các tài liệu theo độ tương đồng (cosine similarity)
    sorted_results = sorted(result_docs, key=lambda x: x['score'], reverse=True)

    return sorted_results


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


# Hàm tìm kiếm sử dụng inverted index trước khi tính toán TF-IDF
def search_shard(query):
    # Tokenize và làm sạch truy vấn
    query_tokens = word_tokenize(query.lower())
    filtered_query = [
        stemmer.stem(word) for word in query_tokens
        if word.isalnum() and word not in stop_words
    ]

    # Bước 1: Tra inverted index đã shard để tìm tài liệu liên quan
    relevant_docs = set()

    for word in filtered_query:
        shard_key = get_shard_word(word)  # Lấy shard key giống như khi indexing

        inverted_doc = inverted_index_shard_collection.find_one({
            "word": word,
            "shard_word": shard_key  # ⚠️ Cần cung cấp shard key khi truy vấn trên collection đã shard
        })

        if inverted_doc:
            relevant_docs.update(inverted_doc['documents'].keys())

    if not relevant_docs:
        return []

    # Bước 2: Lấy nội dung của các tài liệu liên quan
    docs = list(documents_collection.find({"_id": {"$in": list(relevant_docs)}}))

    # Tạo dữ liệu văn bản và danh sách ID
    texts = [doc['title'] + " " + doc['body'] for doc in docs]
    doc_ids = [doc['_id'] for doc in docs]

    # Tính TF-IDF
    tfidf_vectorizer = TfidfVectorizer(stop_words=list(stop_words))
    tfidf_matrix = tfidf_vectorizer.fit_transform(texts)
    query_tfidf = tfidf_vectorizer.transform([query])

    # Cosine similarity
    cosine_similarities = (tfidf_matrix * query_tfidf.T).toarray().flatten()

    # Chuẩn bị kết quả
    result_docs = []
    for i, score in enumerate(cosine_similarities):
        if score > 0:
            result_docs.append({
                "doc_id": doc_ids[i],
                "title": docs[i]['title'],
                "body": docs[i]['body'],
                "score": score
            })

    # Sắp xếp kết quả theo độ tương đồng
    sorted_results = sorted(result_docs, key=lambda x: x['score'], reverse=True)
    return sorted_results


import time

# Câu truy vấn mẫu
query = "machine learning algorithms"

# Đo thời gian chạy của search_plain
start_plain = time.time()
results_plain = search_plain(query)
end_plain = time.time()
print(f"[search_plain] Found {len(results_plain)} results in {end_plain - start_plain:.4f} seconds")

# Đo thời gian chạy của search_shard
start_shard = time.time()
results_shard = search_shard(query)
end_shard = time.time()
print(f"[search_shard] Found {len(results_shard)} results in {end_shard - start_shard:.4f} seconds")
