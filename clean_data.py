import pandas as pd
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
# from google_trans_new import google_translator  

df = pd.read_csv('actress.csv')
print(df)
df_clean = df.dropna(subset=['birthday', 'height', 'cup_size', 'bust', 'waist', 'hips'])
df_clean['height'] = (df['height']).apply(lambda x : float(str(x).split('cm')[0]) * 1.0)
df_clean['bust'] = df['bust'].apply(lambda x : float(str(x).split('cm')[0]) * 1.0)
df_clean['waist'] = df['waist'].apply(lambda x : float(str(x).split('cm')[0]) * 1.0)
df_clean['hips'] = df['hips'].apply(lambda x : float(str(x).split('cm')[0]) * 1.0)
print(df_clean)
# translator = google_translator()
# df_clean['name_en'] = df_clean['name'].apply(translator.translate, lang_tgt='en').apply(getattr, args=('text',))
# df_clean['hobby_en'] = df_clean['hobby'].apply(translator.translate, lang_tgt='en').apply(getattr, args=('text',))

df_clean.to_csv(r'actress_clean.csv', index=False)