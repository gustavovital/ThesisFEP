# Provide the var models for the dataset
#
# Gustavo Vital
# Date: 19-04-2022

# Modules to import
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.api import VAR
from statsmodels.tsa.stattools import adfuller
from statsmodels.tools.eval_measures import rmse, aic

data = pd.read_csv('data\\data_variables.csv')

data_var = data.set_index('date')
data_var.dropna(inplace=True)

# data_var.head()

data_model = data[['gdp_diff', 'cpi_diff', 'ppi', 'interest_diff', 'une_diff', 'lm_positive']]
data_model.dropna(inplace=True)
# Testing models
test_obs = 8
train = data_model[:-test_obs]
test = data_model[-test_obs:]

for i in range(1, 6):  # VAR(1)
    model = VAR(train)
    results = model.fit(i)
    print('Order =', i)
    print('AIC: ', results.aic)
    print('BIC: ', results.bic)
    print()

# SVAR
result = model.fit(3)
result.summary()

# result.plot_acorr()
# plt.show()

irf = result.irf(10)

irf.plot(orth=False, impulse='lm_positive')
plt.show()
