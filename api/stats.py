from math import *
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from pandas.io.json import json_normalize


class Stats(object):

    def get_stats(self, rides):
        """
        Operation corresponding to /stats endpoint, GET request
        :param rides: each rider's rides serialized in json
        :return: csv file with rides grouped by user_id and sorted in descending by
        Euclidian distance of each ride calculated using Haversine formula
        """
        data = self.calc_dist_data(rides)
        data.sort_values(['user_id', 'dist'], ascending=[True, False], inplace=True)
        out_data = data[['from_lat', 'from_lon', 'to_lat', 'to_lon', 'user_id']]
        return out_data.to_csv(index=False)

    def get_chart(self, rides):
        """
        Operation corresponding to /chart endpoint, GET request
        :param rides: each rider's rides serialized in json
        :return: scatter plot, each point describing single rider with X - total rides number (<= size)
        and Y - variance of rides distances
        """
        data = self.calc_dist_data(rides)
        stats = self.calc_stats(data)
        chart = self.create_chart(stats)
        return chart

    @staticmethod
    def calc_stats(data):
        """
        Calculate and add to dataframe statistics for each rider
        :param data: pandas dataframe with from and to coordinates (lat,lon) and distance for each ride
        :return: pandas dataframe with rides variance, mean, standard devition and count for each rider
        """
        stats = data[['user_id', 'dist']].groupby('user_id').agg({'dist': [np.var, np.mean, np.std, np.size]})
        stats.columns = ["_".join(x) for x in stats.columns.ravel()]
        return stats

    @staticmethod
    def create_chart(stats):
        """
        Create scatter plot with X -> rides count, Y -> distance variance
        :param stats: pandas dataframe with rides variance, mean, standard devition and count for each rider
        :return:
        """
        for index, row in (stats[['dist_size', 'dist_var']].iterrows()):
            plt.scatter(row[0], row[1], label=index)
        plt.legend(loc="best")
        plt.xlabel("Rides Count")
        plt.ylabel("Rides Variance")
        plt.title("Rides Statistics")
        figfile = BytesIO()
        plt.savefig(figfile, format='png')
        figfile.seek(0)
        file = figfile.getvalue()
        plt.gcf().clear()
        return file

    @classmethod
    def calc_dist_data(cls, data):
        """
        Calculate and add distance for each ride to dataframe
        :param data:
        :return:
        """
        data = cls.get_dataframe(data)
        data['dist'] = data.apply(lambda row: cls.get_distance(row['from_lon'],
                                                               row['from_lat'], row['to_lon'], row['to_lat']), axis=1)
        return data

    @staticmethod
    def get_dataframe(rides):
        data = json_normalize(rides, 'rides', meta='user_id')
        return data

    @staticmethod
    def get_distance(from_lon, from_lat, to_lon, to_lat):
        # convert decimal degrees to radians
        """
        Calculate Euclidian distance between two points based on geocoordinates using Haversine formula
        :param from_lon: longitude of first point
        :param from_lat: latitude of first point
        :param to_lon: longitude of second point
        :param to_lat: latitude of second point
        :return: distance between two points in km
        """
        from_lon, from_lat, to_lon, to_lat = map(radians, [from_lon, from_lat, to_lon, to_lat])
        # haversine formula
        dlon = to_lon - from_lon
        dlat = to_lat - from_lat
        a = sin(dlat / 2) ** 2 + cos(from_lat) * cos(to_lat) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        km = 6371 * c
        return km
