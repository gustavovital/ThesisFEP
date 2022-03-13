# author: gustavo vital
# date: 11/03/2022
#
# Analysis of speeches with loughran/vader dictionary

import pandas as pd
# import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')

# Data ####
data = pd.read_csv('data\\speeches_data.csv')

# Lexicons ####
# Loughran and Mc Donalds - https://researchdata.up.ac.za/articles/dataset/Loughran_McDonald-SA-2020_Sentiment_Word_List/14401178
loughran = pd.read_csv('data\\LM-SA-2020.csv', index_col=['word'])
# loughran.head()
# loughran.info()
loughran = loughran[(loughran['sentiment'] == 'Negative') | (loughran['sentiment'] == 'Positive')]
# loughran.info()

def count_words(data):
    '''Count the number of words'''
    return len(data.split())

positive = []
negative = []
words_total = []

for row in range(0, (len(data))):

    words_total.append(count_words(data.contents[row]))
    # print('Progress: ' + str(round(((row + 1)/(len(data) + 1))*100, 4)) + '%')

    pos = 0
    neg = 0

    for word in data.iloc[row, 4].split():
        if word in list(loughran.index):
            try:
                if (loughran.loc[word, 'sentiment'] == 'Negative') & (loughran.loc[word, 'sentiment'] == 'Positive'):
                    continue
                elif loughran.loc[word, 'sentiment'] == 'Negative':
                    neg += 1
                else:
                    pos += 1
            except ValueError:
                pass

    positive.append(pos / words_total[row])
    negative.append(neg / words_total[row])


data.insert(len(data.columns), "lm_posiive", positive, True)
data.insert(len(data.columns), "lm_negative", negative, True)

# VADER ----
Analyzer = SentimentIntensityAnalyzer()

pos_vader = []
neg_vader = []
# compound = []

for sentiment in range(len(data)):

    print('Progress: ' + str(round(((sentiment + 1)/(len(data) + 1))*100, 4)) + '%')
    criteria = Analyzer.polarity_scores(data.iloc[sentiment, 4])

    pos_vader.append(criteria['pos'])
    neg_vader.append(criteria['neg'])
    # compound.append(criteria['compound'])


data.insert(len(data.columns), "vader_posiive", pos_vader, True)
data.insert(len(data.columns), "vader_negative", neg_vader, True)
data.insert(len(data.columns), 'words_count', words_total, True)

data.to_csv('data\\data_lexicons.csv', index=False)










