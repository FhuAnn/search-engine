import random
from collections import Counter
from faker import Faker
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from concurrent.futures import ProcessPoolExecutor, as_completed

# Tải các tài nguyên cần thiết từ nltk (nếu chưa tải, bỏ comment)
# nltk.download('punkt')
# nltk.download('stopwords')

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
    content = fake.text(max_nb_chars=3000)  # Tối đa 3000 ký tự
    type_of_doc = random.choice(["article", "webpage", "note"])
    processed_content = preprocess_text(content)
    return {
        "title": title,
        "content": processed_content,
        "type": type_of_doc
    }

# Tính TF-IDF cho danh sách các văn bản
def compute_tfidf(documents):
    tfidf_vectorizer = TfidfVectorizer()
    return tfidf_vectorizer.fit_transform(documents)

# Hàm phân loại bucket dựa trên TF-IDF score (các ngưỡng đã được điều chỉnh)
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

# Hàm xử lý một chunk của document: sinh document, tính TF-IDF và thống kê bucket
def process_chunk(n_docs):
    local_docs = [generate_document() for _ in range(n_docs)]
    processed_contents = [doc["content"] for doc in local_docs]
    tfidf_matrix = compute_tfidf(processed_contents)
    
    chunk_counter = Counter()
    # Với mỗi document, lấy giá trị TF-IDF cao nhất và gán bucket
    for i in range(n_docs):
        tfidf_values = tfidf_matrix[i].toarray()[0]
        max_tfidf = max(tfidf_values)
        # print(max_tfidf)
        bucket = get_tfidf_bucket(max_tfidf)
        chunk_counter[bucket] += 1
    return chunk_counter

# Hàm tổng hợp kết quả từ các chunk
def analyze_tfidf_distribution_parallel(total_docs=10000, chunk_size=1000):
    num_chunks = total_docs // chunk_size
    overall_counter = Counter()
    
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(process_chunk, chunk_size) for _ in range(num_chunks)]
        # Nếu có sàn dư, bạn có thể xử lý thêm một chunk nữa:
        remaining = total_docs % chunk_size
        if remaining:
            futures.append(executor.submit(process_chunk, remaining))
        
        for future in as_completed(futures):
            chunk_counter = future.result()
            overall_counter.update(chunk_counter)
    
    # In ra kết quả thống kê
    for bucket, count in overall_counter.items():
        print(f"{bucket}: {count}")

# Chạy
analyze_tfidf_distribution_parallel(total_docs=10000)
