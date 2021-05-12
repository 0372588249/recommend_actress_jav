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


RETURN_FLDS = ['id', 'age', 'height', 'bust', 'waist', 'hips']
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
                    ['age', str, True, 'Age', 'json'],
                    ['height', str, True, 'Height', 'json'],
                    ['bust', str, True, 'Bust', 'json'],
                    ['waist', str, True, 'Waist', 'json'],
                    ['hips', str, True, 'Hips', 'json']
                ]))

    def post(self):
        data = utils.get_json()
        if 'age' not in data or 'height' not in data or 'bust' not in data or 'waist' not in data or 'hips' not in data:
            return utils.response(400, "Bad request. Missing required fields")

        data = {
            'id': utils.gen_str_id(),
            'age': data['age'],
            'height': data['height'],
            'bust': data['bust'],
            'waist': data['waist'],
            'hips': data['hips'],

        }
        age = data['age']
        height = data['height']
        bust = data['bust']
        waist = data['waist']
        hips = data['hips']
        # db_instance.insert_one('users', data)
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
            datares = res.to_dict(orient='index')
            return datares 

        res = recommend(model, age, height, bust, waist, hips)
        return utils.response(200, "Success", res)

