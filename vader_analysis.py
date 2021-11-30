# Author: gustavovital
# Date: 30/11/2021
#
# The script provides a vader polarity

import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

# get data
press_data = pd.read_pickle('data\\press_data.pkl')

# Initiate Vader
Analyzer = SentimentIntensityAnalyzer()

# create a function to calculate the index
def calculateIndex(data):

    pos = []
    neg = []

    for i in range(len(data)):

        criteria = Analyzer.polarity_scores(data['Doc'][i])

        print('Iteration: ' + str(i))
        # print('negativo: ' + str(criteria['neg']))
        print('positivo: ' + str(criteria['pos']))
        # print('Index: ' + str(criteria['neg']/(criteria['neg'] + criteria['pos'])))
        print('Index: ' + str(criteria['neg']))

        pos.append(criteria['pos'])
        # neg.append(criteria['neg'])

    indiceVader = [y / (x + y) for x, y in zip(pos, neg)]  # define the index as n/(p + n)
    return pos

index_polarity = calculateIndex(press_data)

# plt.plot(index_polarity, 'o-')
# plt.show()

index_data = pd.DataFrame({'date': press_data['Dates'],
                           'title': press_data['title'],
                           'index': index_polarity})

index_data.to_csv("data\\index_data.csv", index=False)
index_data.to_pickle("data\\index_data.pkl")