# Unit root test
#
# Gustavo Vital
# 28-04-2022

# Modules
from statsmodels.tsa.stattools import adfuller
import pandas as pd

# Dataset
data = pd.read_csv('data\\data_variables.csv')

def adf(series):
    for test in ['c', 'ct', 'ctt', 'nc']:
        print('==================================================================')
        print(f'Augmented Dickey-Fuller Test. \nH0: UNIT ROOT\nConstant and trend order to include in regression: {test}\n')
        dftest = adfuller(series.dropna(), autolag='AIC', regression=test)
        dfoutput = pd.Series(
            dftest[0:4],
            index=[
                'Test Statistic',
                'p-value',
                'Lags Used',
                'Number of Observations'
            ],
        )
        for key, value in dftest[4].items():
            dfoutput['Critical value (%s)' % key] = value
        print(dfoutput)
        print('==================================================================')
        if dftest[0] <= dftest[4]['1%']:
            print('Reject H0 at 1%')
        elif dftest[0] <= dftest[4]['5%']:
            print('Reject H0 at 5%')
        elif dftest[0] <= dftest[4]['10%']:
            print('Reject H0 at 10%')
        else:
            print('Do not reject H0.')
        print('==================================================================')

# Check stationarity
for column in data.drop(['words_count'], axis=1).columns[1:len(data.columns)]:
    print('\n')
    print('==================================================================')
    print(f'VARIABLE TO TEST UNIT ROOT: {column}')
    adf(data[column])

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
