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
    trip_index = 0
    subset = gifts.loc[gifts.cluster == cluster]
    s = subset.GiftId.count()
    to = np.zeros([s,3])
    trip_order = pd.DataFrame(to)
    subset['served'] = 0
    subset['trip_id'] = trip_id
    subset['trip_index'] = 0
    subset_sorted = subset.copy()
    subset_sorted = subset_sorted.sort(['Weight'], ascending=[False])
    unserved_gifts = []
    distances = create_distances(subset,False)
    weighted_distances = create_distances(subset,True)
    for index,item in subset_sorted.iterrows():
        # should already be sorted by weight
        unserved_gifts.append(index+1)
    # dataframe of unserved locations
    unserved_df = subset_sorted[subset_sorted['GiftId'].isin(unserved_gifts)]
    # set where we currently are
    c_index = unserved_gifts[0] #  @@ giftID
    c_gift_weight = unserved_df.loc[c_index-1].Weight  # @@ weight
    current_load = current_load + c_gift_weight # @@ weight
    while (unserved_df.GiftId.count() > 0):
        # need to get specific index because it's
        # index of the nearest
        pos_idx = unserved_df.index.get_loc(c_index-1) # @ get the positional index of this gift
        w_near_idx = weighted_distances.loc[pos_idx,:].idxmin()
        weighted_distances.loc[pos_idx,w_near_idx] = 1000000

        current_load = current_load + c_gift_weight # @@ weight
        # now go there
        nearest_gift = unserved_df.iloc[w_near_idx] # @@ gift row

        if nearest_gift.served != 1:
            c_gift_weight = unserved_df.loc[c_index-1].Weight  # @@ weight
            if (current_load + nearest_gift.Weight) < 1000:
                current_load += nearest_gift.Weight
                # set the trip id
                gifts.loc[nearest_gift.name,'trip_id'] = trip_id  # @@ gift index
                # set the gift to served
                gifts.loc[nearest_gift.name,'served'] = True # @@ gift index
                # set the trip index
                gifts.loc[nearest_gift.name,'trip_index'] = trip_index
                # remove the giftId from unserved gifts
                if ((nearest_gift.name+1) in unserved_gifts):
                    unserved_gifts.remove(nearest_gift.name+1) # @@ gift index + 1 = GiftId
                # increase the index
                trip_index += 1
                c_index = nearest_gift.name+1 # @@ gift index + 1 = GiftId
            else: # if the 1000 pound limit has been reached
                # move on to next trip
                trip_id += 1
                # reset the load
                current_load = 0
    print(gifts)
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
    lat_long_b = (row_b.Latitude,row_b.Longitude)
    distance = haversine(lat_long_a,lat_long_b)
    return distance

# @description: create distances and weighted distances matrices
# @param: pandas dataframe
# @return:
def create_distances(subset,weighted):
    subset_copy = subset.copy()
    s = subset['GiftId'].count()
    data = np.zeros([s,s])
    distances = pd.DataFrame(data)
    weighted_distances = pd.DataFrame(data)
    outer_idx = 0
    inner_idx = 0
    for index,item in subset.iterrows():
        inner_idx = 0
        if (outer_idx < subset['GiftId'].count()):
            for index1,item1 in subset.iterrows():
                distance = haver_ab(item,item1)
                distances.iloc[inner_idx,outer_idx] = distance
                # we're gonna be wild and get distances * weight
                if weighted:
                    weighted_distances.iloc[inner_idx,outer_idx] = distances.iloc[inner_idx,outer_idx] * item1.Weight
                inner_idx += 1
            outer_idx += 1
    diag_idx = 0
    for index,item in distances.iterrows():
        weighted_distances.iloc[diag_idx,diag_idx] = 9999999
        diag_idx += 1
    if (weighted):
        return weighted_distances
    else:
        return distances
