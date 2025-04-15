from sklearn.feature_extraction.text import TfidfVectorizer

# Danh sách các tài liệu
documents = [
    "kiana kaslana is a valkyrie",
    "raiden mei is also a valkyrie",
    "bronya zaychik is a genius",
    "seele volleirei loves bronya",
    "murata himeko is a teacher"
]

# Khởi tạo vectorizer
vectorizer = TfidfVectorizer()

# Huấn luyện và biến đổi dữ liệu
tfidf_matrix = vectorizer.fit_transform(documents)

# In ra từ vựng (vocabulary)
print("Từ vựng:", vectorizer.get_feature_names_out())

# In ma trận TF-IDF
print("Ma trận TF-IDF:")
print(tfidf_matrix.toarray())
