import connexion
from connexion import NoContent
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

# instantiate Database and Stats objects
database = Database(coll_limit, db_id, collection_id, MongoProvider())
instance = Stats()


def get(size: int = None):
    """
    Operation corresponding to /get endpoint, GET request
    :param size: optional number of rides (last) for each rider, if not set all available rides are returned
    :return: each rider's rides serialized in json
    """
    data = database.get(size)
    if not data:
        return NoContent, 404
    return data, 200


def store(ride):
    """
    Operation corresponding to /store endpoint, POST request
    :param ride: json with ride to be stored
    :return: added ride serialized in json
    """
    data = database.store(ride)
    if not data:
        return NoContent, 400
    return data, 201


def get_stats(size: int = None):
    """
    Operation corresponding to /stats endpoint, GET request
    :param size: optional number of rides (last) for each rider, if not set all available rides are returned
    :return: csv file with rides grouped by user_id and sorted in descending by
    Euclidian distance of each ride calculated using Haversine formula
    """
    rides = database.get(size)
    if not rides:
        return NoContent, 404
    data = instance.get_stats(rides)
    if not data:
        return NoContent, 500
    return data, 200


def get_chart(size: int = None):
    """
    Operation corresponding to /chart endpoint, GET request
    :param size: optional number of rides (last) for each rider, if not set all available rides are used
    :return: scatter plot, each point describing single rider with X - total rides number (<= size)
    and Y - variance of rides distances
    """
    rides = database.get(size)
    if not rides:
        return NoContent, 404
    chart = instance.get_chart(rides)
    if not chart:
        return NoContent, 500
    return chart, 200


if __name__ == '__main__':
    app = connexion.App(__name__, specification_dir='swagger/')
    app.add_api('app.yaml')
    app.run(port=9090)
