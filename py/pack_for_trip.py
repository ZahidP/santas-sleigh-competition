import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
###
from haversine import haversine
from sklearn.cluster import KMeans
from matplotlib import pyplot


# distance = lambda column1, column2: pd.np.linalg.norm(column1 - column2)
# >>> result = zero_data.apply(lambda col1: zero_data.apply(lambda col2: distance(col1, col2)))

# @description: we're gonna organize trips within clusters
def cluster_trip_creation(cluster,gifts,trip_id,verbose):
    current_load = 0
    number_of_gifts = 0
    subset = gifts.loc[gifts.cluster == cluster]
    # subset = subset.sort(['Weight'], ascending=[False])
    # s = subset['GiftId'].count()
    # data = np.zeros([s,s])
    # distances = pd.DataFrame(data)
    # for index,item in subset.iterrows():
    #     #idx = index + 1
    #     if (idx < subset['GiftId'].count()):
    #         for index1,item1 in subset.iterrows():
    #             distances.iloc[index1,index] = haver_ab(item,item1)

    for index,item in subset.iterrows():
        if item.served != 1:
            if (current_load + item.Weight) < 1000:
                gifts.iloc[index,6] = trip_id
                #gifts.iloc[index,5] = 1
                current_load += item.Weight
            else:
                if verbose:
                    print('Final Trip Weight: ' + str(current_load))
                    print('Trip Id: ' + str(trip_id))
                trip_id += 1
                gifts.iloc[index,6] = trip_id
                current_load = item.Weight
    trip_id += 1
    current_load = 0
    return trip_id


def do_trips(clusters,gifts,run,verbose):
    trip_id = 1
    for i in range(0,clusters):
        if verbose:
            print('Cluster: ' + str(i))
            print('TripId: ' + str(trip_id))
        trip_id = cluster_trip_creation(i,gifts,trip_id,verbose)
        print(trip_id)
    file_name = '../data/' + run + '.csv'
    gifts.to_csv(file_name)
    return gifts

# @description: apply the haversine function to pandas column
# @param: pandas dataframe
# @output: pandas dataframe with distances
def haver_ab(row_a,row_b):
    lat_long_a = (row_a.Latitude,row_a.Longitude)
    #print(lat_long_a)
    lat_long_b = (row_b.Latitude,row_b.Longitude)
    #print(lat_long_b)
    distance = haversine(lat_long_a,lat_long_b)
    return distance

def overrides(gifts1,gifts2):
    gifts2['trip_index'] = 5
    gifts2 = gifts2.iloc[0:20000]
    gifts1 = gifts1.iloc[0:20000]
    gifts1.trip_id = gifts1.trip_id + 1500
    result = pd.merge(gifts1, gifts2, on='GiftId')
    results = results.sort(['TripId','trip_index'], ascending=[False]))
    return result
