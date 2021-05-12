import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn import metrics
from datetime import date
import warnings
warnings.filterwarnings("ignore")

actress = pd.read_csv('actress_clean.csv')
actress['birthday'] = pd.to_datetime(actress['birthday'], yearfirst= True)
todays_date = date.today()
actress['age'] = (todays_date.year - pd.DatetimeIndex(actress['birthday']).year) * 1.0

df = actress[['age', 'height', 'bust', 'waist', 'hips']]
actress_np = df.to_numpy()
k_mean_4 = KMeans(n_clusters=4)
model = k_mean_4.fit(actress_np)
result = k_mean_4.labels_
df1 = actress[['id', 'age', 'height', 'bust', 'waist', 'hips']]
df2 = actress[['id', 'name', 'imgurl', 'birthplace', 'hobby', 'cup_size']]
lookup = df1.merge(df2, on='id', how='left')
lookup['cluster'] = result
def recommend(model, age, height, bust, waist, hips):
    arr = np.array([[age, height, bust, waist, hips]])
    pred = model.predict(arr)
    res = lookup[lookup['cluster'] == pred[0]].sample(10)
    return res


# Input data, you can change input here
#
age = 30
height = 160
bust = 100
waist = 60
hips = 100
# res = recommend(model, age, height, bust, waist, hips)
# print(res)
