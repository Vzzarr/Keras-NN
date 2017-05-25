from gensim.corpora import Dictionary
from os import listdir
import re
import numpy as np


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