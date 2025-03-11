import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download("stopwords")
text ="This is an example sentence demonstrating the removal of stopwords"

stop_words = set(stopwords.words("english"))

words = word_tokenize(text)

filtered_words = [word for word in words if word.lower() not in stop_words]
filtered_text =' '.join(filtered_words)

print(f"Original text: {text}")
print(f"After removal of stopwords: {filtered_words}")