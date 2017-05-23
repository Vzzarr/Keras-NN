import keras.preprocessing.text
import numpy as np

text = np.array(['this is just some random, stupid text'])
print(text.shape)

tk = keras.preprocessing.text.Tokenizer(
        nb_words=2000,
        filters=keras.preprocessing.text.base_filter(),
        lower=True,
        split=" ")

tk.fit_on_texts(text)
pred = tk.texts_to_sequences(text)
print(pred)

model.predict(pred)
