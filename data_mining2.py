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
# print(actress)

df = actress[['height', 'bust', 'waist', 'hips']]
# print(df)

# describe data
#
# print(actress.describe())

# AVG data
#
AVH_HEIGHT = actress.height.mean()
AVH_BUST = actress.bust.mean()
AVH_WAIST = actress.waist.mean()
AVH_HIPS = actress.hips.mean()


# ignore cupsize
#
# print(df.cup_size.value_counts())
# mapper = { 'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 3, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10, 'L': 11, 'M': 12, 'N': 13, 'P': 14 }
# df['cup_size'] = df['cup_size'].map(mapper)
# print(df)

actress_np = df.to_numpy()
# print(actress_np)

# elbow
#
# sum_distance = []
# K = range(1, 13)
# for k in K:
#     k_mean = KMeans(n_clusters=k)
#     k_mean.fit(actress_np)
#     sum_distance.append(k_mean.inertia_)
# plt.plot(K, sum_distance, 'bx-')
# plt.show()

# bad try
#
# k_mean_2 = KMeans(n_clusters=2)
# k_mean_2.fit(actress_np)
# label_2 = k_mean_2.labels_
# print(label_2)
# metrics_silhouette_score_2 = metrics.silhouette_score(actress_np, label_2, metric='euclidean')
# metrics_calinski_2 = metrics.calinski_harabasz_score(actress_np, label_2)
# print(metrics_silhouette_score_2)
# print(metrics_calinski_2)

# best try
#
k_mean_3 = KMeans(n_clusters=3)
model = k_mean_3.fit(actress_np)
result = k_mean_3.labels_
# print(model)
# print(result)
# metrics_silhouette_score_3 = metrics.silhouette_score(actress_np, result, metric='euclidean')
# metrics_calinski_3 = metrics.calinski_harabasz_score(actress_np, result)
# print(metrics_silhouette_score_3)
# print(metrics_calinski_3)

# bad try
#
# k_mean_4 = KMeans(n_clusters=4)
# k_mean_4.fit(actress_np)
# label_4 = k_mean_4.labels_
# print(label_4)
# metrics_silhouette_score_4 = metrics.silhouette_score(actress_np, label_4, metric='euclidean')
# metrics_calinski_4 = metrics.calinski_harabasz_score(actress_np, label_4)
# print(metrics_silhouette_score_4)
# print(metrics_calinski_4)

# bad try
#
# k_mean_5 = KMeans(n_clusters=5)
# k_mean_5.fit(actress_np)
# label_5 = k_mean_5.labels_
# print(label_5)
# metrics_silhouette_score_5 = metrics.silhouette_score(actress_np, label_5, metric='euclidean')
# metrics_calinski_5 = metrics.calinski_harabasz_score(actress_np, label_5)
# print(metrics_silhouette_score_5)
# print(metrics_calinski_5)

# show all clusters
#
# plt.scatter(actress_np[:,0], actress_np[:,3])
# plt.show()

# show clusters plt
#
# plt.scatter(
#     actress_np[result == 0, 0], actress_np[result == 0, 3],
#     c='lightgreen',
#     marker='s',
#     label='cluster 1',
#     edgecolors='black'
# )

# plt.scatter(
#     actress_np[result == 1, 0], actress_np[result == 1, 3],
#     c='orange',
#     marker='o',
#     label='cluster 2',
#     edgecolors='black'
# )

# plt.scatter(
#     actress_np[result == 2, 0], actress_np[result == 2, 3],
#     c='lightblue',
#     marker='v',
#     label='cluster 3',
#     edgecolors='black'
# )
# plt.scatter(
#     model.cluster_centers_[:, 0], model.cluster_centers_[:, 3],
#     marker='*',s=250, 
#     c='red',
#     label='centroids',
#     edgecolors='black'
# )
# plt.legend(scatterpoints=1)
# plt.grid()
# plt.show()

# input: age, height, cup_size, bust, waist, hips
# => output: which cluster?
# random(10) in clusters
#
df1 = actress[['id', 'height', 'bust', 'waist', 'hips']]
# print(df1.info())

df2 = actress[['id', 'name', 'birthday', 'imgurl', 'birthplace', 'hobby', 'cup_size']]
# print(df2)

lookup = df1.merge(df2, on='id', how='left')
# print(lookup.info())
lookup['cluster'] = result
# print(lookup)

# recommend actress function
#
def recommend(model, height=AVH_HEIGHT, bust=AVH_BUST, waist=AVH_WAIST, hips=AVH_HIPS):
    arr = np.array([[height, bust, waist, hips]])
    pred = model.predict(arr)
    res = lookup[lookup['cluster'] == pred[0]].sample(10)
    # translator = google_translator()
    # res['name_english'] = res['name'].apply(translator.translate, lang_src='ja', lang_tgt='en')
    # res['hobby_english'] = res['hobby'].apply(translator.translate, lang_src='ja', lang_tgt='en')
    return res


# Input data, you can change input here
#
height = 165
bust = 105
waist = 50
hips = 105
res = recommend(model, height)
print(res)