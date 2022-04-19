
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('data\\data_variables.csv')

# Descriptive statistic
data.head()

# Correlation


# fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
#
# ax1.plot(data['cpi'], data['vader_positive'], 'o')
# z = np.polyfit(data['cpi'], data['vader_positive'], 1)
# p = np.poly1d(z)
# ax1.plot(data['cpi'],p(data['cpi']),"r--")
#
# ax2.plot(data['cpi'], data['lm_positive'], 'o')
# z = np.polyfit(data['cpi'], data['lm_positive'], 1)
# p = np.poly1d(z)
# ax2.plot(data['cpi'],p(data['cpi']),"r--")
#
# ax3.plot(data['vader_positive'], data['lm_positive'], 'o')
# z = np.polyfit(data['vader_positive'], data['lm_positive'], 1)
# p = np.poly1d(z)
# ax3.plot(data['vader_positive'],p(data['vader_positive']),"r--")
#
#
# plt.show()

# g.map_lower(sns.kdeplot, levels=4, color=".2")



plt.plot(data['cpi'], data['vader_positive'], 'o')
z = np.polyfit(data['cpi'], data['vader_positive'], 1)
p = np.poly1d(z)
plt.plot(data['cpi'],p(data['cpi']),"r--")

plt.show()
