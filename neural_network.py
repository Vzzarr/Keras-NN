from __future__ import print_function

import numpy as np
import keras.preprocessing.text
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.preprocessing.text import Tokenizer
from gensim.corpora import Dictionary
from loadFS import load_input, clean_str, filtro_stringa
from keras.models import load_model
from os import listdir
from keras.utils import plot_model

localNNname = 'nn_amr.h5'

print('Loading data...')
(x_train, y_train), (x_test, y_test), dictionary = \
    load_input("/home/nicholas/Documenti/Keras-NN/mario/training", "/home/nicholas/Documenti/Keras-NN/mario/test")

max_words = 10000
batch_size = 100
epochs = 50

tokenizer = Tokenizer(num_words=max_words)


if(localNNname in listdir('.')) :
    model = load_model(localNNname)
else :
    print(len(x_train), 'train sequences')
    print(len(y_train), 'train sequences')
    print(len(x_test), 'test sequences')
    print(len(y_test), 'test sequences')

    num_classes = np.max(y_train) + 1
    print(num_classes, 'classes')

    print('Vectorizing sequence data...')
    x_train = tokenizer.sequences_to_matrix(x_train, mode='binary')
    x_test = tokenizer.sequences_to_matrix(x_test, mode='binary')
    print('x_train shape:', x_train.shape)
    print('x_test shape:', x_test.shape)

    print('Convert class vector to binary class matrix '
          '(for use with categorical_crossentropy)')
    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)
    print('y_train shape:', y_train.shape)
    print('y_test shape:', y_test.shape)


    print('Building model...')
    model = Sequential()
    model.add(Dense(512, input_shape=(max_words,)))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes))
    model.add(Activation('softmax'))

    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    plot_model(model, to_file='model.png')  #prints the NN into a .png file

    history = model.fit(x_train, y_train,
                        batch_size=batch_size,
                        epochs=epochs,
                        verbose=1,
                        validation_split=0.1)
    score = model.evaluate(x_test, y_test,
                           batch_size=batch_size, verbose=1)
    print('Test score:', score[0])
    print('Test accuracy:', score[1])

    model.save(localNNname)

input = filtro_stringa(open("input.txt", "r").read())
inputDic = Dictionary([input[:-int(len(input) / 2)], input[int(len(input) / 2):]])
dictionary.merge_with(inputDic)

wordsIdInput = []
for word in input :
    wordsIdInput.append(dictionary.token2id[word])
inputbinary = tokenizer.sequences_to_matrix([wordsIdInput], mode='binary')
predictions = model.predict_classes(inputbinary)

print(dictionary.get(predictions[0]))