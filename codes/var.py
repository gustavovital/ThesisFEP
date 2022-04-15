import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.api import VAR
from statsmodels.tsa.stattools import adfuller
from statsmodels.tools.eval_measures import rmse, aic

data = pd.read_csv('data\\data_variables.csv')

data_var = data.set_index('date')
data_var.dropna(inplace=True)
