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
lexicon = lexicon.groupby(pd.PeriodIndex(lexicon['date'], freq='M')).mean().reset_index()
lexicon = lexicon[lexicon['date'] <= '2020-12']
lexicon.drop('words_count', axis=1, inplace=True)

lexicon['date'] = lexicon['date'].dt.strftime('%Y-%m').add('-01 00:00:00.000')
lexicon['date'] = pd.to_datetime(lexicon.date)

# API's: series are in monthly frequncy
API_gdp = 'OECDELORSGPORIXOBSAM'  # Real Gross Domestic Product (Euro/ECU series) for Euro area
API_cpi = 'CPHPTT01EZM659N'  # Consumer Price Index: Harmonized Prices: Total All Items for the Euro Area
API_10y = 'IRLTLT01EZM156N'  # Long-Term Government Bond Yields: 10-year: Main (Including Benchmark) for the Euro Area
API_ppi = 'PIEATI01EZM661N'  # Producer Prices Index: Economic Activities: Total Industrial Activities for the Euro Area
API_une = 'LRHUTTTTEZM156S'  # Harmonized Unemployment Rate: Total: All Persons for the Euro Area
API_cps = 'CSINFT02EZM460S'  # Consumer Opinion Surveys: Consumer Prices: Future Tendency of Inflation: European
# Commission and National Indicators for the Euro Area
API_rec = 'EUROREC'  # OECD based Recession Indicators for Euro Area from the Period following the Peak through the
# Trough


start_date = '2005-01-01'
end_date = '2020-12-01'

# download series
gdp = get_fred(API_gdp, start_date, end_date)
cpi = get_fred(API_cpi, start_date, end_date)
interest = get_fred(API_10y, start_date, end_date)
ppi = get_fred(API_ppi, start_date, end_date)
une = get_fred(API_une, start_date, end_date)
cps = get_fred(API_cps, start_date, end_date)
# recession = get_fred(API_rec, start_date, end_date)

gdp.columns = ['date', 'gdp']
cpi.columns = ['date', 'cpi']
interest.columns = ['date', 'interest']
ppi.columns = ['date', 'ppi']
une.columns = ['date', 'une']
cps.columns = ['date', 'cps']
# recession.columns = ['date', 'recession']

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

# add lexicons info to the data
data = pd.merge(data, lexicon, on='date', how='outer')

# dealing missing and saving data
data['vader_positive'] = data['vader_positive'].interpolate()
data['vader_negative'] = data['vader_negative'].interpolate()
data['lm_positive'] = data['lm_positive'].interpolate()
data['lm_negative'] = data['lm_negative'].interpolate()

# creating data with diff values

data['gdp_diff'] = data['gdp'].diff()
data['cpi_diff'] = data['cpi'].diff()
data['une_diff'] = data['une'].diff()
data['ppi_diff'] = data['ppi'].diff()
data['interest_diff'] = data['interest'].diff()

# dummy for recession
data['subprime'] = np.where((data.date >= '2008-03-01') & (data.date <= '2009-05-01'), 1, 0)
data['debt_crises'] = np.where((data.date >= '2011-09-01') & (data.date <= '2013-01-01'), 1, 0)
data['covid'] = np.where((data.date >= '2020-03-01') & (data.date <= '2020-05-01'), 1, 0)

# cumulaive index
np.mean(data['lm_negative'])

data_model = data[data.date >= '2010-01-01']
data_model.drop('subprime', axis=1, inplace=True)

# save data
data_model.to_csv('data\\data_model.csv', index=False)
data.to_csv('data\\data.csv', index=False)