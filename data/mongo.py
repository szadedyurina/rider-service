from pymongo import *
import pymongo
from bson.json_util import *
from api.stats import get_stats, get_chart
from injector import *

db_id = 'test'
collection_id = 'Riders'


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
            mongo_provider: MongoProvider = None,
            limit: int = 5
    ):
        self.mongo_provider = MongoProvider()
        self.limit = limit
        self.instance = None

    def connection(self) -> MongoClient:
        if not self.instance:
            self.instance = self.mongo_provider.create()
            if not collection_id in self.instance[db_id].collection_names():
                self.instance[db_id].create_collection(collection_id, capped=True, size = 5242880, max=self.limit)
            self.instance[db_id][collection_id].create_index([('user_id', pymongo.ASCENDING)])
        return self.instance

class Ride(object):
    # @inject(db=Database, limit=3)
    def store(self, ride, db:Database = None) -> json:
        if not db: db = Database().connection()
        collection = db[db_id][collection_id]
        data = ride
        ride_id = collection.insert({'user_id': data['user_id'], 'to_lat': data['to_lat'], 'to_long': data['to_long'], 'from_lat': data['from_lat'], 'from_long': data['from_long']})
        inserted_ride = collection.find_one({'_id': ride_id})
        db.close()
        return dumps({'result': inserted_ride['user_id']}, separators=(',', ':'))

    # @inject(db=Database)
    def get(self, size:int, db:Database = None) -> json:
        if not db: db = Database().connection()
        collection = db[db_id][collection_id]
        output = json.loads(dumps(list(collection.find())))
        stats = get_stats(output)
        db.close()
        return stats

    def chart(self, db:Database = None) -> json:
        if not db: db = Database().connection()
        collection = db[db_id][collection_id]
        output = json.loads(dumps(list(collection.find())))
        stats = get_chart(output)
        db.close()
        return stats

instance = Ride()
