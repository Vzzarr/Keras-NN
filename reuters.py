from __future__ import print_function

import numpy as np
import keras.preprocessing.text
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.preprocessing.text import Tokenizer
from loadFS import load_input
from keras.models import load_model
from os import listdir

localNNname = 'cane.h5'

if(localNNname in listdir('.')) :
    model = load_model(localNNname)
else :
    print('Loading data...')
    (x_train, y_train), (x_test, y_test) = \
        load_input("Reuters21578-Apte-90Cat/training", "Reuters21578-Apte-90Cat/test")

    max_words = 10000 #np.amax([np.amax(x_train), np.amax(x_test), np.amax(y_train), np.amax(y_test)])
    batch_size = 32
    epochs = 1

    print(len(x_train), 'train sequences')
    print(len(y_train), 'train sequences')
    print(len(x_test), 'test sequences')
    print(len(y_test), 'test sequences')

    num_classes = np.max(y_train) + 1#len(filter(lambda x: x[0] != '.', listdir("Reuters21578-Apte-90Cat/training")))
    print(num_classes, 'classes')

    print('Vectorizing sequence data...')
    tokenizer = Tokenizer(num_words=max_words)
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
'''
text = np.array(['COLOMBIA BUSINESS ASKED TO DIVERSIFY FROM COFFEE'
                 'BOGOTA, April 8 - A Colombia government trade official has'
                 'urged the business community to aggressively diversify its'
                 'activities and stop relying so heavily on coffee.'
                 'Samuel Alberto Yohai, director of the Foreign Trade'
                 'Institute, INCOMEX, said private businessmen should not become'
                 'what he called "mental hostages" to coffee, traditionally'
                 'Colombia\'s major export.'
                 'The National Planning Department forecast that in 1987'
                 'coffee will account for only one-third of total exports, or'
                 'about 1.5 billion dlrs, with oil and energy products making up'
                 'another third and non-traditional exports the remainder.'])

tk = text.Tokenizer(
        nb_words=2000,
        filters=text.base_filter(),
        lower=True,
        split=" ")

tk.fit_on_texts(text)
prediction = model.predict(np.array(tk.texts_to_sequences(text)))
print(prediction)
'''