import pandas as pd
import numpy as np
from math import *
import matplotlib.pyplot as plt
from pandas.io.json import json_normalize

def get_stats(rides):
    data = json_normalize(rides)
    data['dist'] = data.apply(lambda row: get_distance(row['from_long'],
                                                        row['from_lat'], row['to_long'], row['to_lat']), axis=1)
    data.sort_values(['user_id', 'dist'], ascending=[True, False], inplace=True)
    out_data = data[['from_lat', 'from_long', 'to_lat', 'to_long', 'user_id']]
    return out_data.to_csv(index=False)

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