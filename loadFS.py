from gensim.corpora import Dictionary
from os import listdir
import re
import numpy as np
from stop_words import get_stop_words
import string
from nltk.tokenize import word_tokenize
import nltk
from nltk.stem import SnowballStemmer


def clean_str(stringa):
    stringa = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", stringa)
    stringa = re.sub(r"\'s", " \'s", stringa)
    stringa = re.sub(r"\'ve", " \'ve", stringa)
    stringa = re.sub(r"n\'t", " n\'t", stringa)
    stringa = re.sub(r"\'re", " \'re", stringa)
    stringa = re.sub(r"\'d", " \'d", stringa)
    stringa = re.sub(r"\'ll", " \'ll", stringa)
    stringa = re.sub(r",", "", stringa)
    stringa = re.sub(r"!", "", stringa)
    stringa = re.sub(r"\(", "", stringa)
    stringa = re.sub(r"\)", "", stringa)
    stringa = re.sub(r"\?", "", stringa)
    stringa = re.sub(r"\s{2,}", " ", stringa)
    return stringa.strip().lower()

#
def filtro_stringa(stringa):
    nltk.download('punkt')
    if "ANSA" in stringa :
        stringa = stringa[stringa.index('-') + 1:]
        stringa = stringa[stringa.index('-') + 1:]

    stoplist = get_stop_words('italian')
    filtered_corpus = [word for word in word_tokenize(unicode(clean_str(stringa), "utf-8").lower()) if
                        word not in stoplist and word not in string.punctuation]
    stemmed_corpus = [SnowballStemmer('italian').stem(word) for word in filtered_corpus]

    return stemmed_corpus

def load_input(training_path, test_path) :
    xy_train = []
    xy_test = []

    (x_train, y_train), (x_test, y_test) = ([], []), ([], [])

    for tag in filter(lambda x: x[0] != '.', listdir(training_path)) :
        path = training_path + "/" + tag
        for file in filter(lambda x: x[0] != '.', listdir(path)):
            f = open(path + "/" + file, "r")
            xy_train.append(np.array((clean_str(f.read()) + " " + tag).split()))   #last element of collection is the tag

    for tag in filter(lambda x: x[0] != '.', listdir(test_path)) :
        path = test_path + "/" + tag
        for file in filter(lambda x: x[0] != '.', listdir(path)):
            f = open(path + "/" + file, "r")
            xy_test.append(np.array((clean_str(f.read()) + " " + tag).split()))    #last element of collection is the tag

    vocab_train = Dictionary(xy_train)
    vocab_test = Dictionary(xy_test)
    vocab_train.merge_with(vocab_test)

    for xy in xy_train :
        y = xy[-1]
        y_train.append(vocab_train.token2id[y])
        x = np.delete(xy, -1)
        words = []
        for word in x :
            words.append(vocab_train.token2id[word])
        x_train.append(words)

    for xy in xy_test :
        y = xy[-1]
        y_test.append(vocab_train.token2id[y])
        x = np.delete(xy, -1)
        words = []
        for word in x :
            words.append(vocab_train.token2id[word])
        x_test.append(words)

    return (np.array(x_train), np.array(y_train)), (np.array(x_test), np.array(y_test)), vocab_train


#print(load_input("/home/nicholas/Documenti/Keras-NN/ansa"))