import numpy as np
import re
from gensim.models import KeyedVectors
import nltk
from nltk.corpus import stopwords
import pickle
from xgboost import XGBClassifier
import time
import json
from keras import backend as K
from keras.metrics import Precision, Recall
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Activation, Dropout, Dense, InputLayer, GRU, LSTM

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
print('PUNKT LOADED')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
print('STOPWORDS LOADED')
np.random.seed(11)

def vectorizer_func(word, vectorizer):
    try:
        vec_word = vectorizer.get_vector(word)
    except:
        vec_word = np.zeros(50, dtype=float)
    return vec_word

def right_padding(l, size):
    if len(l) >= size:
        l = l[:size]
    else:
        l.extend([np.zeros(50, dtype=float)]*(size-len(l)))
    # return np.array(l, dtype=object).flatten()
    return np.array(l, dtype=object)

# def pipeline(X, wv, sw, text_size):
#     X1 = [text.split(' ') for text in X]
#     X2 = [[y.lower() for y in x if y not in sw] for x in X1]
#     X3 = [[vectorizer_func(y, wv) for y in x] for x in X2]
#     Xf = np.array([np.array(right_padding(x, text_size)) for x in X3], dtype=float)

#     return Xf

def pipeline(X, wv, sw, text_size):
    X1 = [text.split(' ') for text in X]
    X2 = [[y.lower() for y in x if y not in sw] for x in X1]
    # X2 = [[y.lower() for y in x if y] for x in X1]
    X3 = [[vectorizer_func(y, wv) for y in x] for x in X2]
    Xf = np.array([np.array(right_padding(x, text_size)) for x in X3], dtype=float)

    return Xf

def preprocess_pipeline_train(df, wv, sw, feature_names, target, text_size):
    X = df[feature_names].apply(lambda x: re.sub(r'[^ \nA-Za-zÀ-ÖØ-öø-ÿ/ ]+', ' ', x, 0, re.IGNORECASE))
    y = df[target]

    Xf = pipeline(X, wv=wv, sw=sw, text_size=text_size)
    return Xf, y

def preprocess_pipeline_text(text, wv, sw, text_size):
    X = [re.sub(r'[^ \nA-Za-zÀ-ÖØ-öø-ÿ/ ]+', ' ', text, 0, re.IGNORECASE)]
    print(X)
    Xf = pipeline(X, wv=wv, sw=sw, text_size=text_size)

    return Xf

def createGRU(input_size):
  metrics = ['acc', Precision(), Recall()]
  # loss = tf.keras.losses.CategoricalCrossentropy(from_logits=False)
  loss = tf.keras.losses.BinaryCrossentropy(from_logits=False)
  optim = tf.keras.optimizers.Adam(learning_rate=0.001)

  model = Sequential()
  model.add(InputLayer(input_shape=(input_size,50)))
  model.add(GRU(128, return_sequences=True, dropout=0.1))
  model.add(GRU(64, return_sequences=False, dropout=0.1))
  model.add(Dense(1, activation='sigmoid'))
  # model.add(Dense(6, activation='softmax'))
  model.compile(loss=loss, optimizer=optim, metrics=metrics)

  return model

def createLSTM(input_size):
  metrics = ['acc', Precision(), Recall()]
  loss = tf.keras.losses.BinaryCrossentropy(from_logits=False)
  optim = tf.keras.optimizers.Adam(learning_rate=0.001)

  model = Sequential()
  model.add(InputLayer(input_shape=(input_size,50)))
  model.add(LSTM(128, return_sequences=True, dropout=0.1))
  model.add(LSTM(64, return_sequences=False, dropout=0.1))
  model.add(Dense(1, activation='sigmoid'))
  # model.add(Dense(6, activation='softmax'))
  model.compile(loss=loss, optimizer=optim, metrics=metrics)

  return model

class ITT:
    
    def __init__(self, word_vectorizer=None):
        start_time = time.time()
        if word_vectorizer == None:
            self.word_vectorizer_pt = KeyedVectors.load_word2vec_format('model/glove/glove_s50.txt')
            self.word_vectorizer_en = KeyedVectors.load_word2vec_format('model/glove/glove50dEN')
            # self.word_vectorizer = KeyedVectors.load('model/glove/glove_s50.txt')
        print("GLOVE LOADED --- %s seconds ---" % (time.time() - start_time))
        self.stop_words_pt = set(stopwords.words('portuguese')) 
        self.stop_words_en = set(stopwords.words('english'))
        self.stop_words_pt.add('')
        self.stop_words_en.add('')

        start_time = time.time()
        # self.model = pickle.load(open('model/xgb_itt_model.pkl', "rb"))
        self.model_pt = createGRU(400)
        self.model_pt.load_weights(f'model/PT-BR/model_gru')
        self.model_en = createGRU(25)
        self.model_en.load_weights(f'model/EN/model_gru')
        print("MODEL LOADED --- %s seconds ---" % (time.time() - start_time))

        # self.window = sg.Window('ITTrue')
        # self.output = self.window.FindElement('output')

    def Analyse(self, text, language):

        #Tratamento da equação inputada pelo usuário, transformando-a em uma lista

        #self.news = self.window.Read()

        text = str(text)

        # processed_text = preprocess_pipeline_text(text, wv=self.word_vectorizer, sw=self.stop_words, text_size=400)

        # predictions = [self.model.predict(processed_text), self.model.predict_proba(processed_text)]
        # predictions = [self.model.predict(processed_text), self.model.predict_proba(processed_text)]

        # if predictions[0] == 1:
        if language == 'pt':
            processed_text = preprocess_pipeline_text(text, wv=self.word_vectorizer_pt, sw=self.stop_words_pt, text_size=400)
            output_text = f"{100- self.model_pt.predict(processed_text)[0][0]*100:.2f}"
        elif language == 'en':
            processed_text = preprocess_pipeline_text(text, wv=self.word_vectorizer_en, sw=self.stop_words_en, text_size=25)
            output_text = f"{100- self.model_en.predict(processed_text)[0][0]*100:.2f}"
        # else:
        #     output_text = f"{predictions[1][0][0]*100:.2f}%"

        return output_text
        #Escreve no output o resultado da equação
        # self.output.Update(disabled=False)
        # self.output.Update(output_text)
        # self.output.Update(disabled=True)

        
if __name__ == "__main__":
    ITT = ITT()

    ITT.Analyse()