# Author: Gustavo Vital
# Date: 03/03/2022
#
# Get the speeches and wrangling

#### Modules ####
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#### Get data ####
data = pd.read_csv('C:\\Users\\gusta\\Documents\\Mestrado\\Dissertation\\all_ECB_speeches.csv',
                   encoding='utf-8', sep='|')
# data.head()
# type(data.date)

#### Wrangling ####
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
