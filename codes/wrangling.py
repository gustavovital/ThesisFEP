# final version of data_wrangling. The first file was moved to depreciated folder, as the original version contain
# series and frequencies not used in the word
#
# wrangling: download and manipulate time series to correlate with lexicons to a economic case study
# github: @gustavovital
# 2022-05-08

# modules
import pandas as pd
import numpy as np
import pandas_datareader as pdr
import statsmodels.api as sm


# Get FRED data
def get_fred(serie, start, end):
    df = pdr.DataReader(serie, 'fred', start, end)
    return df.reset_index()


# data
lexicon = pd.read_csv('data\\data_lexicons_clean.csv')
lexicon_M = lexicon.groupby(pd.PeriodIndex(lexicon['date'], freq='M')).mean().reset_index()

# API's: series are in monthly frequncy
API_gdp = 'OECDELORSGPORIXOBSAM'  # Real Gross Domestic Product (Euro/ECU series) for Euro area
API_cpi = 'CPHPTT01EZM659N'  # Consumer Price Index: Harmonized Prices: Total All Items for the Euro Area
API_10y = 'IRLTLT01EZM156N'  # Long-Term Government Bond Yields: 10-year: Main (Including Benchmark) for the Euro Area
API_ppi = 'PIEATI01EZM661N'  # Producer Prices Index: Economic Activities: Total Industrial Activities for the Euro Area
API_une = 'LRHUTTTTEZM156S'  # Harmonized Unemployment Rate: Total: All Persons for the Euro Area
API_cps = 'CSINFT02EZM460S'  # Consumer Opinion Surveys: Consumer Prices: Future Tendency of Inflation: European
# Commission and National Indicators for the Euro Area


start_date = '1998-01-01'
end_date = '2020-12-01'

# download series
gdp = get_fred(API_gdp, start_date, end_date)
cpi = get_fred(API_cpi, start_date, end_date)
interest = get_fred(API_10y, start_date, end_date)
ppi = get_fred(API_ppi, start_date, end_date)
une = get_fred(API_une, start_date, end_date)
cps = get_fred(API_cps, start_date, end_date)

gdp.columns = ['date', 'gdp']
cpi.columns = ['date', 'cpi']
interest.columns = ['date', 'interest']
ppi.columns = ['date', 'ppi']
une.columns = ['date', 'une']
cps.columns = ['date', 'cps']


# get non observable variables
gdp_cycle, gdp_trend = sm.tsa.filters.hpfilter(gdp.gdp, 14400)  # hodrick-prescott filter to get the gap gdp.
# lambda parameter = 1440 (M)


# creating data frame of the series
data = pd.DataFrame({'date': gdp['date'],
                     'gdp': gdp['gdp'],
                     'cpi': cpi['cpi'],
                     'interest': interest['interest'],
                     'ppi': ppi['ppi'],
                     'une': une['une'],
                     'cps': cps['cps'],
                     'gdp_cycle': gdp_cycle,
                     'gdp_trend': gdp_trend})

# first filtering (date > 2005 because of the lexicons range)
data = data[data.date >= '2005-01-01']
data.reset_index(inplace=True)
data.drop(columns=['index'], inplace=True)

# add lexicons info to the data
data['lm_positive'] = lexicon.lm_positive
data['lm_negative'] = lexicon.lm_negative
data['vader_positive'] = lexicon.vader_positive
data['vader_negative'] = lexicon.vader_negative
data['words_count'] = lexicon.words_count

# creating dummies for the data
data['covid'] = np.where((data.date >= '2020-01-01') & (data.date <= '2021-04-01'), 1, 0)
data['recession'] = np.where(((data.date >= '2008-01-01') & (data.date <= '2009-06-30')) |
                               ((data.date >= '2011-07-01') & (data.date <= '2013-01-01')) |
                               ((data.date >= '2019-10-01') & (data.date <= '2020-06-30')), 1, 0)

# cleaning data from missing and saving data
data.dropna(inplace=True)
data.to_csv('data\\data.csv', index=False)
