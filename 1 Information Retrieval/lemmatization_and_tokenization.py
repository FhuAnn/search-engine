import nltk 
nltk.download('punkt_tab')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
#tokennization
sentence ="the bats were hanging by their feet"
tokenized_words = nltk.word_tokenize(sentence)

print(f"Tokenized sentence = {tokenized_words}")

lemmatizer =WordNetLemmatizer()

lemmatized_words = [lemmatizer.lemmatize(word) for word in tokenized_words]

print(f"Lemmatized words = {lemmatized_words}")