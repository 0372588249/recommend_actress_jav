import re
import utils
import time
import pymongo
from flask_restplus import Resource, Namespace
from database.mongo import db_instance
from configuration.config import app_config
from werkzeug.security import generate_password_hash
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn import metrics
from datetime import date
import warnings

import csv
import json


RETURN_FLDS = ['id', 'height', 'bust', 'waist', 'hips']
users_ns = Namespace('users', description='Users')


def filter_response_data(data):
    return {key:value for key,value in data.items() if key in RETURN_FLDS}


@users_ns.route('')
class Users(Resource):
    @users_ns.doc(responses={ 200: 'OK', 500: 'Internal Server Error' })
    def get(self):
        users = list(db_instance.find('users').sort('created_at', pymongo.DESCENDING))
        users = [filter_response_data(x) for x in users]
        return utils.response(200, "Success", users)

    
    @users_ns.doc(responses={ 200: 'OK', 400: 'Bad request. Missing required fields', 500: 'Internal Server Error' }, 
                parser=utils.get_doc_parser([
                    ['height', str, True, 'Height', 'json'],
                    ['bust', str, True, 'Bust', 'json'],
                    ['waist', str, True, 'Waist', 'json'],
                    ['hips', str, True, 'Hips', 'json']
                ]))

    def post(self):
        data = utils.get_json()
        if 'height' not in data or 'bust' not in data or 'waist' not in data or 'hips' not in data:
            return utils.response(400, "Bad request. Missing required fields")

        data = {
            'id': utils.gen_str_id(),
            'height': data['height'],
            'bust': data['bust'],
            'waist': data['waist'],
            'hips': data['hips'],

        }
        height = data['height']
        bust = data['bust']
        waist = data['waist']
        hips = data['hips']
        # db_instance.insert_one('users', data)
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
            res = res.fillna('')
            datares = res.to_dict(orient='records')
            print(datares)
            return datares 

        res = recommend(model, height, bust, waist, hips)
        return utils.response(200, "Success", res)

