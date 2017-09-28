from pymongo import *
from pymongo.collection import *
import pymongo
from bson.json_util import *
import configparser

config = configparser.ConfigParser()
config.read('appconfig.ini')

# get db and collection names
db_id = config['Mongo']['db_id']
collection_id = config['Mongo']['collection_id']


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
            provider: MongoProvider = None
    ):
        self.mongo_provider = provider or MongoProvider()
        self.instance = None
        self.limit = limit

    def connection(self) -> MongoClient:
        if not self.instance:
            self.instance = self.mongo_provider.create()
            self.instance[db_id][collection_id].create_index([('user_id', pymongo.ASCENDING)])
        return self.instance

    @property
    def collection(self) -> Collection:
        connection = self.connection()
        return connection[db_id][collection_id]

    def store(self, ride) -> json:
        coll = self.collection
        # update rider document with new ride if the document exists or create new document and add first ride otherwise
        rider_coll = coll.find_one_and_update(
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
            coll.update_one(
                {'user_id': ride['user_id']},
                {'$inc': {'count': -1},
                 '$pop': {'rides': -1}})
        inserted_doc = coll.find_one({'user_id': ride['user_id']}, {'rides': {'$slice': -1}})
        return json.loads(dumps({'Updated rider': inserted_doc}))

    def get(self, size: int) -> json:
        coll = self.collection
        if size:
            output = json.loads(dumps(list(coll.find({}, {'rides': {'$slice': -size}}))))
        else:
            output = json.loads(dumps(list(coll.find())))
        return output
