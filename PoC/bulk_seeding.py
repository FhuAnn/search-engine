import pymongo
from faker import Faker
import random
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk

# Đảm bảo tải các tài nguyên cần thiết từ nltk
nltk.download('punkt')
nltk.download('stopwords')

# Kết nối MongoDB
conn = "mongodb://localhost:27100,localhost:27200"
client = pymongo.MongoClient(conn)
db = client["search_engine"]
collection = db["documents"]

# Tạo Faker và công cụ xử lý văn bản
fake = Faker()
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

# Xử lý văn bản: tokenize, remove stopwords, stemming
def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [stemmer.stem(word) for word in tokens if word.isalpha() and word not in stop_words]
    return ' '.join(tokens)

# Tạo document giả
def generate_document():
    title = fake.sentence(nb_words=6)
    content = fake.text(max_nb_chars=500)
    type_of_doc = random.choice(["article", "webpage", "note"])
    processed_content = preprocess_text(content)
    return {
        "title": title,
        "content": processed_content,
        "type": type_of_doc
    }

# Tính TF-IDF
def compute_tfidf(documents):
    tfidf_vectorizer = TfidfVectorizer()
    return tfidf_vectorizer.fit_transform(documents)

# Phân loại bucket từ TF-IDF
def get_tfidf_bucket(score):
    if score < 0.05:
        return "very_low"
    elif score < 0.10:
        return "low"
    elif score < 0.15:
        return "medium_low"
    elif score < 0.20:
        return "low_medium"
    elif score < 0.30:
        return "medium"
    elif score < 0.40:
        return "high_medium"
    elif score < 0.50:
        return "high"
    else:
        return "very_high"


# Seeding dữ liệu
def seed_data(batch_size=1000, total_docs=10000):
    bulk_data = []
    documents = []

    for _ in range(total_docs):
        doc = generate_document()
        bulk_data.append(doc)
        documents.append(doc["content"])

        if len(bulk_data) == batch_size:
            tfidf_matrix = compute_tfidf(documents)
            for i, doc in enumerate(bulk_data):
                tfidf_values = tfidf_matrix[i].toarray()[0]
                max_tfidf = max(tfidf_values)
                doc["tfidf_score"] = float(max_tfidf)  # <--- Lưu score thực
                doc["tfidf_bucket"] = get_tfidf_bucket(max_tfidf)

            collection.insert_many(bulk_data)
            print(f"Inserted {len(bulk_data)} documents with tfidf_bucket...")
            bulk_data = []
            documents = []

    # Xử lý phần còn lại
    if bulk_data:
        tfidf_matrix = compute_tfidf(documents)
        for i, doc in enumerate(bulk_data):
            tfidf_values = tfidf_matrix[i].toarray()[0]
            max_tfidf = max(tfidf_values)
            doc["tfidf_score"] = float(max_tfidf)  # <--- Lưu score thực
            doc["tfidf_bucket"] = get_tfidf_bucket(max_tfidf)

        collection.insert_many(bulk_data)
        print(f"Inserted {len(bulk_data)} documents with tfidf_bucket...")

# Chạy seeding
seed_data(total_docs=10000)
