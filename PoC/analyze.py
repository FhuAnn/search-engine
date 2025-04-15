import random
from collections import Counter
from faker import Faker
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk

# Tải dữ liệu NLTK
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('punkt_tab')

# Tạo Faker và công cụ xử lý văn bản
fake = Faker()
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

# Xử lý văn bản
def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [stemmer.stem(word) for word in tokens if word.isalpha() and word not in stop_words]
    return ' '.join(tokens)

# Tạo document giả
def generate_document():
    title = fake.sentence(nb_words=6)
    content = fake.text(max_nb_chars=3000)
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

# Phân loại bucket
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


# Hàm chính
def analyze_tfidf_distribution(total_docs=10000):
    documents = [generate_document() for _ in range(total_docs)]
    processed_contents = [doc["content"] for doc in documents]

    tfidf_matrix = compute_tfidf(processed_contents)

    bucket_counter = Counter()

    for i in range(total_docs):
        tfidf_values = tfidf_matrix[i].toarray()[0]
        max_tfidf = max(tfidf_values)
        bucket = get_tfidf_bucket(max_tfidf)
        bucket_counter[bucket] += 1

    # In kết quả thống kê
    for bucket, count in bucket_counter.items():
        print(f"{bucket}: {count}")

# Chạy
analyze_tfidf_distribution(total_docs=10000)
