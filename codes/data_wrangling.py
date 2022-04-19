
# Modules to import
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader as pdr

# Get FRED data
def get_fred(serie, start_date, end_date):

    df = pdr.DataReader(serie, 'fred', start_date, end_date)
    return df.reset_index()

# Data
lexicon = pd.read_csv('data\\data_lexicons_clean.csv')
lexicon = lexicon.groupby(pd.PeriodIndex(lexicon['date'], freq='Q')).mean().reset_index()

# APIs
API_gdp = 'CLVMEURSCAB1GQEA19'  # quartly
API_cpi = 'CPHPTT01EZM659N'     # monthly
API_10y = 'IRLTLT01EZM156N'     # monthly
API_ppi = 'OECDPIEAMP02GYM'     # monthly
API_une = 'LRHUTTTTEZM156S'     # monthly
API_cps = 'CSINFT02EZM460S'     # monthly

start_date = '1998-01-01'
end_date = '2022-01-01'

gdp = get_fred(API_gdp, start_date, end_date)
cpi = get_fred(API_cpi, start_date, end_date)
interest = get_fred(API_10y, start_date, end_date)
ppi = get_fred(API_ppi, start_date, end_date)
une = get_fred(API_une, start_date, end_date)
cps= get_fred(API_cps, start_date, end_date)

gdp.columns = ['date', 'gdp']
cpi.columns = ['date', 'cpi']
interest.columns = ['date', 'interest']
ppi.columns = ['date', 'ppi']
une.columns = ['date', 'une']
cps.columns = ['date', 'cps']

# Wrangling
gdp_diff = pd.DataFrame({'date':gdp['date'][1:], 'gdp':gdp['gdp'].diff()})  # get the diff

# Other series
cpi = pd.DataFrame({'date': gdp['date'], 'cpi': cpi.groupby(pd.PeriodIndex(cpi['date'], freq="Q"))['cpi'].mean().reset_index()['cpi'][:-1]})
interest = pd.DataFrame({'date': gdp['date'], 'interest': interest.groupby(pd.PeriodIndex(interest['date'], freq="Q"))['interest'].mean().reset_index()['interest'][:-1]})
ppi = pd.DataFrame({'date': gdp['date'], 'ppi': ppi.groupby(pd.PeriodIndex(ppi['date'], freq="Q"))['ppi'].mean().reset_index()['ppi'][:-1]})
une = pd.DataFrame({'date': gdp['date'], 'une': une.groupby(pd.PeriodIndex(une['date'], freq="Q"))['une'].mean().reset_index()['une'][:-1]})
cps = pd.DataFrame({'date': gdp['date'], 'cps': cps.groupby(pd.PeriodIndex(cps['date'], freq="Q"))['cps'].mean().reset_index()['cps'][:-1]})

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

# Creating dataframe

data = pd.DataFrame({'date':gdp['date'],
                     'gdp_diff':gdp_diff['gdp'],
                     'cpi':cpi['cpi'],
                     'interest':interest['interest'],
                     'ppi':ppi['ppi'],
                     'une':une['une'],
                     'cps':cps['cps']})

data = data[28:]  # From 2005

data.reset_index(inplace=True)
data.drop(columns=['index'], inplace=True)

data['lm_positive'] = lexicon.lm_positive
data['lm_negative'] = lexicon.lm_negative
data['vader_positive'] = lexicon.vader_positive
data['vader_negative'] = lexicon.vader_negative
data['words_count'] = lexicon.words_count
data['recession'] = np.where(((data.date >= '2008-01-01') & (data.date <= '2009-06-30')) |
         ((data.date >= '2011-07-01') & (data.date <= '2013-01-01')) |
         ((data.date >= '2019-10-01') & (data.date <= '2020-06-30')), 1, 0)


# fig, axs = plt.subplots(2, 5)
# count = 1
# for i in range(0,2):
#     for j in range(0,5):
#         # print(count)
#         axs[i, j].plot(data['date'], data[data.columns[count]])
#         axs[i, j].set_title(data.columns[count])
#         count += 1

'''Stationary variables of the dataframe data:

The dataframe data is saved (above) as data_variables.
At  1%:     gdp_diff (c, ct, ctt, nc)
            lm_positive (c, ct, ctt)  
            vader_positive (c, ct, ctt)   
            cpi_diff (nc)
            une_diff (c, nc)
            ppi_diff (nc)
            interest_diff (c, ct, ctt, nc)
            cps_diff (c, ct, ctt, cn)
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
'''

data['cpi_diff'] = data['cpi'].diff()
data['une_diff'] = data['une'].diff()
data['ppi_diff'] = data['ppi'].diff()
data['interest_diff'] = data['interest'].diff()
data['cps_diff'] = data['cps'].diff()

# Save data to csv
data.dropna(inplace=True)
data.to_csv('data\\data_variables.csv', index=False)


