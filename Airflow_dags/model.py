import os

#disable tensorflow unwanted warnings and info
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout, Bidirectional
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
import numpy as np
import tensorflow.keras.utils as ku
import airflow_config


def train_model():

    #reading the data
    file = open(airflow_config.MODEL_DATA, 'r')
    data = file.read()
    corpus = data.split("\n")

    tokenizer = Tokenizer(oov_token = '<OOV>')
    tokenizer.fit_on_texts(corpus)

    #adding 1 for the oov_token
    total_words = len(tokenizer.word_index) + 1

    #generating input sequences
    input_sequences = []
    for line in corpus:
        tokenized_sentence = tokenizer.texts_to_sequences([line])[0]
        for i in range(1, len(tokenized_sentence)):
            n_gram_sequence = tokenized_sentence[:i+1]
            input_sequences.append(n_gram_sequence)
    
    #padding tokenized sentences
    max_sequence_len = max([len(x) for x in input_sequences])
    input_sequences = pad_sequences(input_sequences, maxlen = max_sequence_len, padding = 'pre')

    train_inputs, labels = input_sequences[:, :-1], input_sequences[:, -1]
    labels = ku.to_categorical(labels, num_classes = total_words)

    #defining the model
    model = Sequential([
        Embedding(total_words, 64, input_length=max_sequence_len-1),
        Bidirectional(LSTM(20, return_sequences = True)),
        Dropout(0.2),
        Bidirectional(LSTM(20)),
        Dense(64, activation = 'relu'),
        Dense(total_words, activation = 'softmax')
    ])

    #compiling
    model.compile(loss = 'categorical_crossentropy', 
        optimizer = Adam(learning_rate = 0.001), metrics = ['accuracy'])
    
    history = model.fit(train_inputs, labels, epochs = 100, verbose = 1)

    seed_text = airflow_config.POEM_SEED
    next_words = airflow_config.NUM_GENERATED_WORDS

    for _ in range(next_words):
        tokenized_sentence = tokenizer.texts_to_sequences([seed_text])[0]
        tokenized_sentence = pad_sequences([tokenized_sentence], maxlen=max_sequence_len - 1, padding = 'pre')
        predicted = np.argmax(model.predict(tokenized_sentence))
        output_word = ""
        for word, index in tokenizer.word_index.items():
            if index == predicted:
                output_word = word
                break
        seed_text += " " + output_word
    
    with open(airflow_config.CONFIG_DIR + 'generated_poem.txt', 'w') as f:
        f.write(seed_text)

    



