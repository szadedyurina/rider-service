from pymongo import *
import pymongo
from bson.json_util import *
from api.stats import get_stats, get_chart
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
            mongo_provider: MongoProvider = None,
            limit: int = 5
    ):
        self.mongo_provider = MongoProvider()
        self.limit = limit
        self.instance = None

    def connection(self) -> MongoClient:
        if not self.instance:
            self.instance = self.mongo_provider.create()
            self.instance[db_id][collection_id].create_index([('user_id', pymongo.ASCENDING)])
        return self.instance


class Ride(object):
    # @inject(db=Database, limit=3)
    def store(self, ride, db: Database = None) -> json:
        if not db:
            db = Database()
            connection = db.connection()
        collection = connection[db_id][collection_id]
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
        if rider_coll['count'] > db.limit:
            collection.update_one(
                {'user_id': ride['user_id']},
                {'$inc': {'count': -1},
                 '$pop': {'rides': -1}})
        inserted_doc = collection.find_one({'user_id': ride['user_id']}, {'rides': {'$slice': -1}})
        connection.close()
        return json.loads(dumps({'Updated rider': inserted_doc}))

    # @inject(db=Database)
    def get(self, size: int, db: Database = None) -> json:
        if not db: db = Database().connection()
        collection = db[db_id][collection_id]
        output = json.loads(dumps(list(collection.find({}, {'rides': {'$slice': -size}}))))
        db.close()
        return output

    def get_stats(self, size: int, db: Database = None):
        output = self.get(size, db)
        stats = get_stats(output)
        return stats

    def chart(self, db: Database = None):
        if not db: db = Database().connection()
        collection = db[db_id][collection_id]
        output = json.loads(dumps(list(collection.find())))
        stats = get_chart(output)
        db.close()
        return stats


instance = Ride()
