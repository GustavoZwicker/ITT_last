# import numpy as np
# import re
# from gensim.models import KeyedVectors
# import nltk
# from nltk.corpus import stopwords
# import pickle
# from xgboost import XGBClassifier
# import time
# import json

# word_vectorizer = KeyedVectors.load_word2vec_format('model/glove/glove_s50.txt')
# word_vectorizer.save('glove_s50')
from dash import Dash, dash_table
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

print(df)
