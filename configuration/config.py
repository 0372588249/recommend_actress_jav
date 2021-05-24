import os 


class BaseConfig:
    API_HOST = '0.0.0.0'
    API_PORT = 18050
    BASE_URL = "http://localhost:18050/"

    TMP_DIR = 'static/tmp'

class DevConfig(BaseConfig):
    mongo_host = '127.0.0.1'
    mongo_port = 27017
    mongo_dbname = 'recommend_actress_jav'

class StagingConfig(BaseConfig):
    mongo_host = '10.40.80.68'
    mongo_port = 31000
    mongo_dbname = 'recommend_actress_jav'

if 'ENV' in os.environ:
    if os.environ['ENV'] == 'dev':
        app_config = DevConfig()
    elif os.environ['ENV'] == 'staging':
        app_config = StagingConfig()
else:
    app_config = DevConfig()
