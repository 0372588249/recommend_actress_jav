import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import date
import warnings
warnings.filterwarnings("ignore")

actress = pd.read_csv('actress_clean.csv')
actress['birthday'] = pd.to_datetime(actress['birthday'], yearfirst= True)
todays_date = date.today()
actress['age'] = todays_date.year - pd.DatetimeIndex(actress['birthday']).year

# Min age
print(actress.age.min())
print(actress[actress['age'] == actress.age.min()])

# Max age
print(actress.age.max())
print(actress[actress['age'] == actress.age.max()])

# AVG age
print(actress.describe())

# Analisis age pyplot
# plt.figure(figsize=(15, 10))
# sns.displot(actress.age)
# plt.show()

# Find actress row by name
print(actress[actress.name.str.contains('JULIA')])