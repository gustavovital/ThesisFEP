# Author: gustavovital
# Date: 30/11/2021
#
# The script provides a vader polarity

import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')


# get data
press_data = pd.read_pickle('data\\press_data.pkl')
speeches_data =pd.read_pickle('data\\speeches_data.pkl')

# Initiate Vader
Analyzer = SentimentIntensityAnalyzer()

# create a function to calculate the index
# def calculateIndex(data, doc):
#     pos = []
#
#     for i in range(len(data)):
#
#         # define polarity
#         criteria = Analyzer.polarity_scores(data[doc][i])
#         # extract the positive polarity from vader
#         pos.append(criteria['pos'])
#     # return positive polarity
#     return pos


# teste
# calculateIndex(speeches_data, 'contents')
# criteria = Analyzer.polarity_scores(speeches_data.iloc[0, 4])

pos = []
for i in range(len(speeches_data)):
    print(i)
    criteria = Analyzer.polarity_scores(speeches_data.iloc[i, 4])
    pos.append(criteria['compound'])


plt.plot(pos)
plt.show()
# FAZER COM ILOC/LOC
# --


# index_polarity = calculateIndex(press_data, 'Doc')
#
# plt.plot(index_polarity, 'o')
# plt.show()
#
# index_data = pd.DataFrame({'date': press_data['Dates'],
#                            'title': press_data['title'],
#                            'index': index_polarity})
#
# index_data.to_csv("data\\index_data.csv", index=False)
# index_data.to_pickle("data\\index_data.pkl")