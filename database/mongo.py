import pymongo 
from configuration.config import app_config
from database.schema import DB_SCHEMA


class MongoDatabaseUtils:
    def __init__(self, mongo_uri, database_name, schema):
        self.mongo_client = pymongo.MongoClient(mongo_uri)
        self.database = self.mongo_client[database_name]
        self.schema = schema


    # private method
    def _check_scheme(self, data, c_schema):
        for key, value in data.items():
            if type(value) != c_schema[key]['type']:
                raise Exception("Invalid type for field %s, expected %s but got %s" % (key, c_schema[key]['type'], type(value)))


    # private method
    def _filter_data(self, data, c_schema):
        filtered_data = {key:value for key, value in data.items() if key in c_schema}
        return filtered_data


    # private method
    def _filter_update_fields(self, data, c_schema):
        filtered_data = {key:value for key, value in data.items() if key in c_schema and \
                        not ('update' in c_schema[key] and not c_schema[key]['update'])}
        return filtered_data


    # private method
    def _get_update_data(self, update_data, c_schema):
        if '$set' in update_data and c_schema is not None:
            filterd_data = self._filter_data(update_data['$set'], c_schema)
            filterd_data = self._filter_update_fields(filterd_data, c_schema)
            self._check_scheme(filterd_data, c_schema)
            update_data['$set'] = filterd_data
        return update_data


    # private method
    def _get_insert_data(self, data, c_schema):
        if c_schema is None:
            filtered_data = data 
        else:
            filtered_data = [self._filter_data(x, c_schema) for x in data]
            for x in filtered_data:
                self._check_scheme(x, c_schema)
        return filtered_data


    # private method
    def _get_collection_schema(self, collection_name):
        return self.schema[collection_name] if collection_name in self.schema else None


    def insert(self, collection_name, data):
        c_schema = self._get_collection_schema(collection_name)
        filtered_data = self._get_insert_data(data, c_schema)
        return self.database[collection_name].insert_many(filtered_data)


    def insert_one(self, collection_name, data):
        return self.insert(collection_name, [data])


    def find(self, collection_name, condition={}):
        return self.database[collection_name].find(condition)


    def find_one(self, collection_name, condition={}):
        return self.database[collection_name].find_one(condition)


    def aggregate(self, collection_name, condition):
        return self.database[collection_name].aggregate(condition)


    def update(self, collection_name, condition, update_data):
        c_schema = self._get_collection_schema(collection_name)
        update_data = self._get_update_data(update_data, c_schema)
        return self.database[collection_name].update_many(condition, update_data)


    def bulk_update(self, collection_name, conditions, updates):
        c_schema = self._get_collection_schema(collection_name)
        bulk = self.database[collection_name].initialize_unordered_bulk_op()
        for condition, update_data in zip(conditions, updates):
            update_data = self._get_update_data(update_data, c_schema)
            bulk.find(condition).update(update_data)
        bulk.execute()


    def delete(self, collection_name, condition):
        return self.database[collection_name].delete_many(condition)


    def delete_one(self, collection_name, condition):
        return self.database[collection_name].delete_one(condition)


db_instance = MongoDatabaseUtils(mongo_uri=app_config.mongo_uri, database_name=app_config.mongo_dbname, schema=DB_SCHEMA)
