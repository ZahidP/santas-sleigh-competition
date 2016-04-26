import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
# import sys
###
from haversine import haversine
# from sklearn.cluster import KMeans
# from matplotlib import pyplot
import time



# @description: we're gonna organize trips within clusterss
def cluster_trip_creation(cluster, gifts, trip_id, verbose):
    (counter, current_load, number_of_gifts, trip_index) = (0, 0, 0, 0)
    subset = gifts.loc[gifts.cluster == cluster]
    s = subset.GiftId.count()
    t_arr = []
    # initialize values
    subset.loc[:, 'served'] = 0
    subset.loc[:, 'trip_id'] = trip_id
    subset.loc[:, 'trip_index'] = 0
    subset_sorted = subset.copy()
    subset_sorted = subset_sorted.sort(['Weight'], ascending=[False])
    unserved_gifts = []
    unserved_constant = []
    # multiplied distance by weight of the gift being delivered there
    weighted_distances = create_distances(subset_sorted, True)
    for index, item in subset_sorted.iterrows():
        # should already be sorted by weight
        unserved_gifts.append(index+1)
        unserved_constant.append(index+1)
    # dataframe of unserved locations
    unserved_df = subset_sorted.loc[subset_sorted['GiftId'].isin(unserved_gifts)]
    # set where we currently are
    c_index = unserved_gifts[0]  # @@ giftID
    c_gift_weight = unserved_df.loc[c_index-1].Weight  # @@ weight
    current_load = current_load + c_gift_weight  # @@ weight
    gifts.loc[gifts['GiftId'] == c_index, 'trip_index'] = trip_index
    gifts.loc[gifts['GiftId'] == c_index, 'served'] = True  # @@ gift index
    weighted_distances.loc[0, :] = 0
    trip_index += 1
    # current_load = current_load + c_gift_weight # @@ weight
    while (len(unserved_gifts) > 1):
        t1 = time.time()
        # need to get specific index because it's
        # index of the nearest
        pos_idx = unserved_df.index.get_loc(c_index-1)  # @ get the positional index of this gift
        weighted_distances.loc[pos_idx, :] = 0
        widx = weighted_distances.loc[:, pos_idx].idxmax()
        weighted_distances.loc[widx, pos_idx] = 0
        # now go there
        nearest_gift = unserved_df.iloc[widx]  # @@ gift row
        # print('nearest')
        # print(nearest_gift.GiftId)
        if (counter > s-1):
            break
        if nearest_gift.served is not True:
            c_gift_weight = unserved_df.loc[c_index-1].Weight  # @@ weight
            if (current_load + nearest_gift.Weight) > 1000:
                # if the 1000 pound limit has been reached
                # move on to next trip
                print(current_load)
                trip_id += 1
                # reset the load
                current_load = 0
            current_load += nearest_gift.Weight
            # set the trip id
            gifts.loc[nearest_gift.name, 'trip_id'] = trip_id  # @@ gift index
            # set the gift to served
            gifts.loc[nearest_gift.name, 'served'] = True  # @@ gift index
            # set trip index for ordering
            gifts.loc[gifts['GiftId'] == nearest_gift.GiftId, 'trip_index'] = trip_index
            # remove the giftId from unserved gifts
            if ((nearest_gift.name+1) in unserved_gifts):
                unserved_gifts.remove(nearest_gift.GiftId)  # @@ gift index + 1 = GiftId
            # increase the index
            trip_index += 1
            c_index = nearest_gift.name + 1  # @@ gift index + 1 = GiftId
        counter += 1
        t2 = time.time()
        t3 = t1 - t2
        t_arr.append(t3)
    # print('avg loop time')
    # avg_time = sum(t_arr)/float(len(t_arr))
    # print(avg_time)
    if (verbose):
        print(avg_time)
        print('unserved_df')
        print(gifts[gifts.cluster == cluster].sort(['Weight'], ascending=[False]))
    trip_id += 1
    current_load = 0
    return trip_id


def do_trips(clusters, gifts, run, verbose, trip_id):
    for i in range(0, clusters):
        if verbose:
            print('Cluster: ' + str(i))
            print('TripId: ' + str(trip_id))
        trip_id = cluster_trip_creation(i, gifts, trip_id, verbose)
        print(trip_id)
    file_name = '../submissions/' + run + '.csv'
    gifts.to_csv(file_name)
    return gifts


# @description: apply the haversine function to pandas column
# @param: pandas dataframe
# @output: pandas dataframe with distances
def haver_ab(row_a, row_b):
    lat_long_a = (row_a.Latitude, row_a.Longitude)
    lat_long_b = (row_b.Latitude, row_b.Longitude)
    distance = haversine(lat_long_a, lat_long_b)
    return distance


# @description: create distances and weighted distances matrices
# @param: pandas dataframe
# @return:
def create_distances(subset, weighted):
    start1 = time.time()
    s = subset['GiftId'].count()
    data = np.zeros([s, s])
    distances = pd.DataFrame(data)
    weighted_distances = pd.DataFrame(data)
    outer_idx = 0
    inner_idx = 0
    for index, item in subset.iterrows():
        inner_idx = 0
        if (outer_idx < subset['GiftId'].count()):
            for index1, item1 in subset.iterrows():
                distance = haver_ab(item, item1)
                distances.iloc[inner_idx, outer_idx] = distance
                # we're gonna be wild and get distances * weight
                if weighted:
                    if (distances.iloc[inner_idx, outer_idx]) != 0:
                        # here we assign the extra weighted cost
                        weighted_distances.iloc[inner_idx, outer_idx] = ((2000/(distances.iloc[inner_idx, outer_idx])) + item1.Weight*2)
                    else:
                        weighted_distances.iloc[inner_idx, outer_idx] = 0
                inner_idx += 1
            outer_idx += 1
    if (weighted):
        return weighted_distances
    else:
        return distances
    end1 = time.time()
    print('weighted matrix time:')
    print(end1 - start1)
