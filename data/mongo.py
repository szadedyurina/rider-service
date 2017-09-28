from pymongo import *
from pymongo.collection import *
import pymongo
from bson.json_util import *
from injector import *

db_id = 'test'
collection_id = 'Rides'


class MongoProvider(object):
    def __init__(self, host: str = None, port: int = None):
        self.host = host
        self.port = port

    def create(self) -> MongoClient:
        return MongoClient(
            self.host, self.port
        )


class Database(object):

    def __init__(
            self,
            limit: int,
            mongo_provider: MongoProvider = None
    ):
        if not MongoProvider: self.mongo_provider = MongoProvider()
        else: self.mongo_provider = mongo_provider
        self.instance = None
        self.db = None
        self.collection = None
        self.limit = limit

    def connection(self) -> MongoClient:
        if not self.instance:
            self.instance = self.mongo_provider.create()
            self.instance[db_id][collection_id].create_index([('user_id', pymongo.ASCENDING)])
        return self.instance

    def get_collection(self)-> Collection:
        connection = self.connection()
        return connection[db_id][collection_id]


    def store(self, ride) -> json:
        collection = self.get_collection()
        # update rider document with new ride if the document exists or create new document and add first ride otherwise
        rider_coll = collection.find_one_and_update(
            {'user_id': ride['user_id']},
            {'$inc': {'count': 1},
             '$push': {'rides': {'to_lat': ride['to_lat'], 'to_lon': ride['to_lon'],
                                 'from_lat': ride['from_lat'], 'from_lon': ride['from_lon']}}},
            fields={'count': 1},
            upsert=True,
            new=True,
            return_document=ReturnDocument.AFTER)

        # check if the rides limit exceeded and drop the first (chronologically) ride if so
        if rider_coll['count'] > self.limit:
            collection.update_one(
                {'user_id': ride['user_id']},
                {'$inc': {'count': -1},
                 '$pop': {'rides': -1}})
        inserted_doc = collection.find_one({'user_id': ride['user_id']}, {'rides': {'$slice': -1}})
        return json.loads(dumps({'Updated rider': inserted_doc}))

    def get(self, size: int) -> json:
        collection = self.get_collection()
        output = json.loads(dumps(list(collection.find({}, {'rides': {'$slice': -size}}))))
        return output
