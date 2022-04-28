# Get economic series and merge with sentiments
#
# Gustavo Vital
# 21-04-2022


# Modules to import
import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
import pandas_datareader as pdr
import statsmodels.api as sm


# Get FRED data
def get_fred(serie, start, end):
    df = pdr.DataReader(serie, 'fred', start, end)
    return df.reset_index()


# Data
lexicon = pd.read_csv('data\\data_lexicons_clean.csv')

lexicon_Q = lexicon.groupby(pd.PeriodIndex(lexicon['date'], freq='Q')).mean().reset_index()
lexicon_M = lexicon.groupby(pd.PeriodIndex(lexicon['date'], freq='M')).mean().reset_index()

# lexicon_M.head()
# plt.plot(lexicon_M['vader_positive'])
# plt.plot(lexicon_M['lm_positive'])
#
# plt.plot(lexicon_M['lm_positive'], lexicon_M['vader_positive'], 'o')

# APIs
API_gdp = 'CLVMEURSCAB1GQEA19'  # quartly
API_gdpm = 'OECDELORSGPORIXOBSAM'  # monthly
API_cpi = 'CPHPTT01EZM659N'  # monthly
API_10y = 'IRLTLT01EZM156N'  # monthly
API_ppi = 'OECDPIEAMP02GYM'  # monthly
API_une = 'LRHUTTTTEZM156S'  # monthly
API_cps = 'CSINFT02EZM460S'  # monthly

start_date = '1998-01-01'
end_date = '2022-01-01'

gdp_Q = get_fred(API_gdp, start_date, end_date)
gdp_M = get_fred(API_gdpm, start_date, end='2022-11-01')
cpi = get_fred(API_cpi, start_date, end_date)
interest = get_fred(API_10y, start_date, end_date)
ppi = get_fred(API_ppi, start_date, end_date)
une = get_fred(API_une, start_date, end_date)
cps = get_fred(API_cps, start_date, end_date)

gdp_Q.columns = ['date', 'gdp']
gdp_M.columns = ['date', 'gdp']
cpi.columns = ['date', 'cpi']
interest.columns = ['date', 'interest']
ppi.columns = ['date', 'ppi']
une.columns = ['date', 'une']
cps.columns = ['date', 'cps']

# Wrangling
gdp_Q_cycle, gdp_Q_trend = sm.tsa.filters.hpfilter(gdp_Q.gdp, 1600)  # lambda = 1600 (Q)
gdp_Q_diff = pd.DataFrame({'date': gdp_Q['date'][1:], 'gdp': gdp_Q['gdp'].diff()})  # get the diff

gdp_M_cycle, gdp_M_trend = sm.tsa.filters.hpfilter(gdp_M.gdp, 14400)  # lambda = 1440 (M)
gdp_M_diff = pd.DataFrame({'date': gdp_M['date'], 'gdp': gdp_M['gdp'].diff()})  # get the diff

# plt.plot(gdp_M.date, gdp_M.gdp)
# plt.plot(gdp_M.date, gdp_M_trend)
# plt.show()

# Other series

# QUARTER SERIES

cpi_Q = pd.DataFrame({'date': gdp_Q['date'],
                      'cpi': cpi.groupby(pd.PeriodIndex(cpi['date'], freq="Q"))['cpi'].mean().reset_index()['cpi'][
                             :-1]})
interest_Q = pd.DataFrame({'date': gdp_Q['date'], 'interest':
    interest.groupby(pd.PeriodIndex(interest['date'], freq="Q"))['interest'].mean().reset_index()['interest'][:-1]})
ppi_Q = pd.DataFrame({'date': gdp_Q['date'],
                      'ppi': ppi.groupby(pd.PeriodIndex(ppi['date'], freq="Q"))['ppi'].mean().reset_index()['ppi'][
                             :-1]})
une_Q = pd.DataFrame({'date': gdp_Q['date'],
                      'une': une.groupby(pd.PeriodIndex(une['date'], freq="Q"))['une'].mean().reset_index()['une'][
                             :-1]})
cps_Q = pd.DataFrame({'date': gdp_Q['date'],
                      'cps': cps.groupby(pd.PeriodIndex(cps['date'], freq="Q"))['cps'].mean().reset_index()['cps'][
                             :-1]})

# plots
# fig, axs = plt.subplots(3, 2)
# axs[0, 0].plot(gdp_diff['date'], gdp_diff['gdp'])
# axs[0, 0].set_title('gdp_diff')
# axs[0, 1].plot(gdp['date'], gdp['gdp'])
# axs[0, 1].set_title('gdp')
# axs[1, 0].plot(cpi['date'], cpi['cpi'])
# axs[1, 0].set_title('cpi')
# axs[1, 1].plot(interest['date'], interest['interest'])
# axs[1, 1].set_title('interest')
# axs[2, 0].plot(ppi['date'], ppi['ppi'])
# axs[2, 0].set_title('ppi')
# axs[2, 1].plot(une['date'], une['une'])
# axs[2, 1].set_title('une')

# Creating dataframe QUARTER
data_Q = pd.DataFrame({'date': gdp_Q['date'],
                       'gdp_diff': gdp_Q_diff['gdp'],
                       'cpi': cpi_Q['cpi'],
                       'interest': interest_Q['interest'],
                       'ppi': ppi_Q['ppi'],
                       'une': une_Q['une'],
                       'cps': cps_Q['cps'],
                       'gdp_gap': gdp_Q_cycle})

data_Q = data_Q[28:]  # From 2005

data_Q.reset_index(inplace=True)
data_Q.drop(columns=['index'], inplace=True)

data_Q['lm_positive'] = lexicon.lm_positive
data_Q['lm_negative'] = lexicon.lm_negative
data_Q['vader_positive'] = lexicon.vader_positive
data_Q['vader_negative'] = lexicon.vader_negative
data_Q['words_count'] = lexicon.words_count
data_Q['recession'] = np.where(((data_Q.date >= '2008-01-01') & (data_Q.date <= '2009-06-30')) |
                               ((data_Q.date >= '2011-07-01') & (data_Q.date <= '2013-01-01')) |
                               ((data_Q.date >= '2019-10-01') & (data_Q.date <= '2020-06-30')), 1, 0)

# Creating dataframe MONTHLY
data_M = pd.DataFrame({'date': gdp_M['date'],
                       'gdp_diff': gdp_M_diff['gdp'],
                       'cpi': cpi['cpi'],
                       'interest': interest['interest'],
                       'ppi': ppi['ppi'],
                       'une': une['une'],
                       'cps': cps['cps'],
                       'gdp_gap': gdp_M_cycle})

data_M = data_M[83:]  # From 2005

data_M.reset_index(inplace=True)
data_M.drop(columns=['index'], inplace=True)

data_M['lm_positive'] = lexicon.lm_positive
data_M['lm_negative'] = lexicon.lm_negative
data_M['vader_positive'] = lexicon.vader_positive
data_M['vader_negative'] = lexicon.vader_negative
data_M['words_count'] = lexicon.words_count
data_M['recession'] = np.where(((data_M.date >= '2008-01-01') & (data_M.date <= '2009-06-30')) |
                               ((data_M.date >= '2011-07-01') & (data_M.date <= '2013-01-01')) |
                               ((data_M.date >= '2019-10-01') & (data_M.date <= '2020-06-30')), 1, 0)

# fig, axs = plt.subplots(2, 5)
# count = 1
# for i in range(0,2):
#     for j in range(0,5):
#         # print(count)
#         axs[i, j].plot(data['date'], data[data.columns[count]])
#         axs[i, j].set_title(data.columns[count])
#         count += 1

'''Stationary variables of the QUARTER dataframe data: 

The dataframe data is saved (above) as data_variables.
At  1%:     gdp_diff (c, ct, ctt, nc)
            lm_positive (c, ct, ctt)  
            vader_positive (c, ct, ctt)   
            cpi_diff (nc)
            une_diff (c, nc)
            ppi_diff (nc)
            interest_diff (c, ct, ctt, nc)
            cps_diff (c, ct, ctt, cn)
            gdp_cycle (c, ct, ctt, cn)
    5%:     ppi (c)
            cpi_diff (c, ct)
            une_diff (ct)
            ppi_diff (c, ct)
    10%:    interest (ct)
            ppi (ctt)
            lm_negative (c)
            cpi_diff (ctt)
            une_diff (ctt)
            ppi_diff (ctt)
            cps (c)

Non stationary variables:   cpi, une, vader_negative

------------------------------------------------------------------------

Stationary variables of the MONTHLY dataframe data: .

At  1%:     lm_positive (c, ct, ctt)   
            lm_negative (c, ct, ctt) 
            vader_positive (c, ct, ctt)
            vader_negative (c, ct, ctt)
            gdp_diff (c, ct, ctt, nc)
            cpi_diff (c, ct, ctt, nc)
            interest_diff (c, ct, ctt, nc)
            une_diff (nc),
            cps_diff (c, ct, ctt, nc)
            gdp_gap (c, ct, nc)
    5%:     ppi (c, ct, nc)    
            gdp_gap (ctt)
    10%:    ppi (ctt)   
            une_diff (c) 
            cps (c)
    
Non stationary variables: cpi, interest, une, cps  
'''

# For the quarter series
data_Q['cpi_diff'] = data_Q['cpi'].diff()
data_Q['une_diff'] = data_Q['une'].diff()
data_Q['ppi_diff'] = data_Q['ppi'].diff()
data_Q['interest_diff'] = data_Q['interest'].diff()
data_Q['cps_diff'] = data_Q['cps'].diff()

# For the monthly series
data_M['cpi_diff'] = data_M['cpi'].diff()
data_M['interest_diff'] = data_M['interest'].diff()
data_M['cps_diff'] = data_M['cps'].diff()
data_M['une_diff'] = data_M['une'].diff()

# dummies for quarter and monthly series
data_Q['subprime'] = np.where((data_Q.date >= '2008-10-01') & (data_Q.date <= '2009-07-01'), 1, 0)
data_Q['covid'] = np.where((data_Q.date >= '2020-01-01') & (data_Q.date <= '2021-04-01'), 1, 0)

data_M['subprime'] = np.where((data_M.date >= '2008-10-01') & (data_M.date <= '2009-07-01'), 1, 0)
data_M['covid'] = np.where((data_M.date >= '2020-01-01') & (data_M.date <= '2021-04-01'), 1, 0)

# Save data to csv
data_Q.dropna(inplace=True)
data_M.dropna(inplace=True)

data_Q.to_csv('data\\data_Q_variables.csv', index=False)
data_M.to_csv('data\\data_M_variables.csv', index=False)
