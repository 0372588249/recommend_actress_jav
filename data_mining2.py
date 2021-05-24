import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn import metrics
from google_trans_new import google_translator
from datetime import date
import warnings
warnings.filterwarnings("ignore")
actress = pd.read_csv('actress_clean.csv')
df = actress[['height', 'bust', 'waist', 'hips']]
AVH_HEIGHT = actress.height.mean()
AVH_BUST = actress.bust.mean()
AVH_WAIST = actress.waist.mean()
AVH_HIPS = actress.hips.mean()
actress_np = df.to_numpy()
k_mean_3 = KMeans(n_clusters=3)
model = k_mean_3.fit(actress_np)
result = k_mean_3.labels_
df1 = actress[['id', 'height', 'bust', 'waist', 'hips']]
df2 = actress[['id', 'name', 'birthday', 'imgurl', 'birthplace', 'hobby', 'cup_size']]
lookup = df1.merge(df2, on='id', how='left')
lookup['cluster'] = result
def recommend(model, height=AVH_HEIGHT, bust=AVH_BUST, waist=AVH_WAIST, hips=AVH_HIPS):
    arr = np.array([[height, bust, waist, hips]])
    pred = model.predict(arr)
    res = lookup[lookup['cluster'] == pred[0]].sample(10)
    return res


# Input data, you can change input here
#
height = 165
bust = 105
waist = 50
hips = 105
res = recommend(model, height)
print(res)