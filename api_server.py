from flask import Flask
from flask_cors import CORS
from flask_restplus import Api
from bson.objectid import ObjectId
import datetime
from configuration.config import app_config
import json


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, set):
            return list(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)


api_app = Flask(__name__)
CORS(api_app, supports_credentials=True)
api_app.json_encoder = JSONEncoder
swagger = Api(app=api_app, doc='/docs/swagger')


from controllers.users import users_ns

swagger.add_namespace(users_ns)

if __name__ == "__main__":
    api_app.run(host=app_config.API_HOST, port=app_config.API_PORT, debug=True)
