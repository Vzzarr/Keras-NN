from gensim.corpora import Dictionary
from os import listdir
import re


def clean_str(string):
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", "", string)
    string = re.sub(r"!", "", string)
    string = re.sub(r"\(", "", string)
    string = re.sub(r"\)", "", string)
    string = re.sub(r"\?", "", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()

def load_input(training_path, test_path) :
    (x_train, y_train), (x_test, y_test) = ([], []), ([], [])

    for tag in filter(lambda x: x[0] != '.', listdir(training_path)) :
        path = training_path + "/" + tag
        for file in filter(lambda x: x[0] != '.', listdir(path)):
            f = open(path + "/" + file, "r")
            x_train.append(f.read())
            y_train.append(tag)

    for tag in filter(lambda x: x[0] != '.', listdir(test_path)) :
        path = test_path + "/" + tag
        for file in filter(lambda x: x[0] != '.', listdir(path)):
            f = open(path + "/" + file, "r")
            x_test.append(f.read())
            y_test.append(tag)


    texts = x_train + y_train + x_test + y_test
    vocab = Dictionary(x_train[0].split())
    print(vocab)

    #return [[vocab.token2id[word] for word in sent] for sent in texts]#(x_train, y_train), (x_test, y_test)

load_input("Reuters21578-Apte-90Cat/training", "Reuters21578-Apte-90Cat/test")