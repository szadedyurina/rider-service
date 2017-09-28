import pandas as pd
import numpy as np
from math import *
import matplotlib.pyplot as plt
from io import BytesIO
from pandas.io.json import json_normalize
from data.mongo import MongoProvider, Database

database = Database(5, MongoProvider())


def get(size: int):
    return database.get(size)

def store(ride):
    return database.store(ride)

def get_stats(size: int):
    rides = database.get(size)
    data = get_dist_data(rides)
    data.sort_values(['user_id', 'dist'], ascending=[True, False], inplace=True)
    out_data = data[['from_lat', 'from_lon', 'to_lat', 'to_lon', 'user_id']]
    return out_data.to_csv(index=False)


def get_chart(size: int):
    rides = database.get(size)
    data = get_dist_data(rides)
    stats = data[['user_id', 'dist']].groupby('user_id').agg({'dist': ['count', 'mean', 'var', 'std']})
    plt.scatter(stats['dist']['count'], stats['dist']['var'])
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    return figfile.getvalue()


def get_dist_data(rides):
    data = json_normalize(rides, 'rides', meta='user_id')
    data['dist'] = data.apply(lambda row: get_distance(row['from_lon'],
                                                       row['from_lat'], row['to_lon'], row['to_lat']), axis=1)
    return data


def get_distance(lon1, lat1, lon2, lat2):
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return km
