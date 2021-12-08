# The script provide a 'tokenization' for the press conferences and for selected words
#
# Author: Gustavo Vital
# Data: 07/12/2021

# Modules required
import pandas as pd
import nltk
from nltk import ngrams

# dataset
press_data = pd.read_pickle('data\\press_data.pkl')

# n-grams
n = 2
bigrams = ngrams(press_data['Doc'][0].split(), n)

for grams in bigrams:
    print(grams)

# -----------------------------------------------------------------------------

tokens = nltk.word_tokenize(press_data['Doc'][0].split())

punkt