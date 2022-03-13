# author: gustavo vital
# date: 11/03/2022
#
# Analysis of speeches with loughran dictionary

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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


# print(count_words(data.iloc[1,4]))

# positive = 0
# negative = 0

# for word in data.iloc[0, 4].split():
#     if word in list(loughran.index):
#         try:
#             if ((loughran.loc[word, 'sentiment'] == 'Negative') & (loughran.loc[word, 'sentiment'] == 'Positive')):
#                 continue
#             elif loughran.loc[word, 'sentiment'] == 'Negative':
#                 negative += 1
#             else:
#                 positive += 1
#         except ValueError:
#             pass


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

    count = count_words(data.iloc[row, 4])
    positive.append(pos / count)
    negative.append(neg / count)

plt.plot(negative, '-')


data.insert(len(data.columns), "positive", positive, True)
data.insert(len(data.columns), "negative", negative, True)

data['index'] = data['positive']/data['negative']

#
data.to_csv('data\\data_loughran.csv', index=False)


for count in range(len(data)):

    words_total.append(count_words(data.contents[count]))

