import pandas as pd

# Data ####
data = pd.read_csv('speeches_data.csv')

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

for row in range(0, len(data)):

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
