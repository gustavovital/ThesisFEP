
# Modules to import
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader as pdr

# Get FRED data
def get_fred(serie, start_date, end_date):

    df = pdr.DataReader(serie, 'fred', start_date, end_date)
    return df.reset_index()


API_gdp = 'CLVMEURSCAB1GQEA19'  # quartly
API_cpi = 'CPHPTT01EZM659N'     # monthly
API_10y = 'IRLTLT01EZM156N'     # monthly
API_ppi = 'OECDPIEAMP02GYM'     # monthly
API_une = 'LRHUTTTTEZM156S'     # monthly

start_date = '1998-01-01'
end_date = '2022-01-01'

gdp = get_fred(API_gdp, start_date, end_date)
cpi = get_fred(API_cpi, start_date, end_date)
interest = get_fred(API_10y, start_date, end_date)
ppi = get_fred(API_ppi, start_date, end_date)
une = get_fred(API_une, start_date, end_date)

gdp.columns = ['date', 'gdp']
cpi.columns = ['date', 'cpi']
interest.columns = ['date', 'interest']
ppi.columns = ['date', 'ppi']
une.columns = ['date', 'une']

# Wrangling
gdp_diff = pd.DataFrame({'date':gdp['date'][1:], 'gdp':gdp['gdp'].diff()})  # get the diff

# Other series
cpi = pd.DataFrame({'date': gdp['date'], 'cpi': cpi.groupby(pd.PeriodIndex(cpi['date'], freq="Q"))['cpi'].mean().reset_index()['cpi'][:-1]})
interest = pd.DataFrame({'date': gdp['date'], 'interest': interest.groupby(pd.PeriodIndex(interest['date'], freq="Q"))['interest'].mean().reset_index()['interest'][:-1]})
ppi = pd.DataFrame({'date': gdp['date'], 'ppi': ppi.groupby(pd.PeriodIndex(ppi['date'], freq="Q"))['ppi'].mean().reset_index()['ppi'][:-1]})
une = pd.DataFrame({'date': gdp['date'], 'une': une.groupby(pd.PeriodIndex(une['date'], freq="Q"))['une'].mean().reset_index()['une'][:-1]})

fig, axs = plt.subplots(3, 2)
axs[0, 0].plot(gdp_diff['date'], gdp_diff['gdp'])
axs[0, 0].set_title('')
axs[0, 1].plot(gdp['date'], gdp['gdp'])
axs[0, 1].set_title('Axis [0, 1]')
axs[1, 0].plot(x, -y, 'tab:green')
axs[1, 0].set_title('Axis [1, 0]')
axs[1, 1].plot(x, -y, 'tab:red')
axs[1, 1].set_title('Axis [1, 1]')



