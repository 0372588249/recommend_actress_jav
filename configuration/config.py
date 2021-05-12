import os 


class BaseConfig:
    API_HOST = '0.0.0.0'
    API_PORT = 18050
    BASE_URL = "http://localhost:18050/"

    STATIC_FOLDER = 'static'
    TMP_DIR = 'static/tmp'

    JWT_SECRET = 'grd41@10ThnVNG'
    PERMISSIONS = type('obj', (object,), {'NORMAL' : 1, 'ADMIN': 1024})

    flask_log_config = {'LOG_FILE': 'logs/api.log'}

    fileupload_url = 'https://upload.thaison.grdai.vn/files/upload'
    fileupload_baseurl = 'https://upload.thaison.grdai.vn/files/'


class DevConfig(BaseConfig):
    mongo_host = '127.0.0.1'
    mongo_port = 27017
    mongo_dbname = 'recommend_actress_jav'
    mongo_uri = 'mongodb://%s:%d' % (mongo_host, mongo_port)


class StagingConfig(BaseConfig):
    mongo_host = '10.40.80.68'
    mongo_port = 31000
    mongo_dbname = 'recommend_actress_jav'
    mongo_user = "root"
    mongo_pass = "root123456"
    mongo_uri = 'mongodb://%s:%s@%s:%d/%s' % (mongo_user, mongo_pass, mongo_host, mongo_port, mongo_dbname)


if 'ENV' in os.environ:
    if os.environ['ENV'] == 'dev':
        app_config = DevConfig()
    elif os.environ['ENV'] == 'staging':
        app_config = StagingConfig()
else:
    app_config = DevConfig()
