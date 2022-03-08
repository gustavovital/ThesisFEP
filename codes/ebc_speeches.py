# Author: Gustavo Vital
# Date: 28/02/2022
#
# Get the speeches and wrangling

# Modules ####
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests

# Get data NOT RUN ####
# req = requests.get('https://www.ecb.europa.eu/press/key/shared/data/all_ECB_speeches.csv')
# url = req.content
# csv = open('data\\all_ECB_speeches.csv', 'wb')
#
# csv.write(url)
# csv.close()

data = pd.read_csv('data\\all_ECB_speeches.csv', encoding='utf-8', sep='|')
# data.head()
# type(data.date)

# Wrangling ####
# Convert date column to date_time
data['date'] = pd.to_datetime(data.date)
# remove missing
data.dropna(inplace=True)
# Filter for date < '2021-12-31' (until 2021)
data = data[data['date'] <= '2021-12-31']

# Filter for recession periods
data['recession'] = np.where(((data.date >= '2008-01-01') & (data.date <= '2009-06-30')) |
         ((data.date >= '2011-07-01') & (data.date <= '2013-01-01')) |
         ((data.date >= '2019-10-01') & (data.date <= '2020-06-30')), 1, 0)

plt.plot(data.date, data.recession)
plt.show()

data.to_pickle("data\\speeches_data.pkl")
data.to_csv("data\\speeches_data.csv", index=False)
