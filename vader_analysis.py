# Author: gustavovital
# Date: 30/11/2021
#
# The script provides a vader polarity

import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

# get data
press_data = pd.read_pickle('data\\press_data.pkl')
press_data.to_csv("data\\press_data.csv", index=False)

# Initiate Vader
Analyzer = SentimentIntensityAnalyzer()

# create a function to calculate the index
def calculateIndex(data, doc):
    pos = []

    for i in range(len(data)):

        # define polarity
        criteria = Analyzer.polarity_scores(data[doc][i])
        # extract the positive polarity from vader
        pos.append(criteria['pos'])
    # return positive polarity
    return pos

# teste
import ast
criteria = Analyzer.polarity_scores(data['contents'].apply(ast.literal_eval).str.decode("utf-8"))

# FAZER COM ILOC/LOC
# --

index_polarity = calculateIndex(press_data, 'Doc')

plt.plot(index_polarity, 'o')
plt.show()

index_data = pd.DataFrame({'date': press_data['Dates'],
                           'title': press_data['title'],
                           'index': index_polarity})

index_data.to_csv("data\\index_data.csv", index=False)
index_data.to_pickle("data\\index_data.pkl")