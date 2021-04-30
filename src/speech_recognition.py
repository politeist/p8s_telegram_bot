from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

stopWords = set(stopwords.words("english"))
words = word_tokenize(text)
freqTable = dict()
sentences = sent_tokenize(text)
sentenceValue = dict()
