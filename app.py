import connexion
from connexion.resolver import RestyResolver
from data.mongo import MongoProvider, Database
from api.stats import Stats
import configparser

# get database name, collection name
config = configparser.ConfigParser()
config.read('appconfig.ini')

coll_limit = int(config['Mongo']['Limit'])
db_id = config['Mongo']['db_id']
collection_id = config['Mongo']['collection_id']

# instantiate Stats object
database = Database(coll_limit, db_id, collection_id, MongoProvider())
instance = Stats(database)

if __name__ == '__main__':
    app = connexion.App(__name__, specification_dir='swagger/')
    app.add_api('app.yaml')
    app.run(port=9090)



