import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
###
from haversine import haversine
from sklearn.cluster import KMeans
from matplotlib import pyplot
import time

# start = time.time()
# end = time.time()
# print(end - start)

# @description: need to caculate distances for cost function
# @param: pandas dataframe
# @output: pandas dataframe with distances
def distances():
    north_pole = (90,0)
    gifts = pd.read_csv('../data/gifts.csv')
    gifts['distance'] = gifts.apply(haver,axis=1)
    gifts.loc[:,'served'] = 0
    gifts.loc[:,'TripId'] = 0
    return gifts

# @description: apply the haversine function to pandas column
# @param: pandas dataframe
# @output: pandas dataframe with distances
def haver(row):
    north_pole = (90,0)
    lat_long = (row.Latitude,row.Longitude)
    distance = haversine(north_pole,lat_long)
    return distance


# @description: would like to cluster to break down into sub problems
# @param: pandas dataframe
# @param: number of clusters, default: 100
# @output: pandas dataframe with cluster number column
# notes:
# ## because the cost function changes with the amount being carried we might need to
# ## find more even weight distributions for  clusters
# ## more thought has to go into this somehow...
def clustering(gifts,n_clusters):
    # k-means now
    lat_long = gifts[['Latitude','Longitude']]
    km = KMeans(init='k-means++', n_clusters = n_clusters, n_init=10)
    newfit = km.fit(lat_long)
    labels = newfit.labels_
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cmhot = plt.get_cmap("hot")
    cax = ax.scatter(lat_long['Longitude'],lat_long['Latitude'], c=labels, cmap=cmhot)
    plt.show()
    gifts.loc[:,'cluster'] = labels
    return gifts

def run_all(runs,gifts,do_trips):
    #gifts = distances()
    trip_id = 1
    gifts_ret = []
    if 1 in runs:
        start1 = time.time()
        gifts_ret.append(gifts.iloc[0:1000])
        gifts_ret[0] = clustering(gifts_ret[0],100)
        gifts_ret[0] = do_trips(100,gifts_ret[0],'run_g1',False,trip_id)
        end1 = time.time()
        print(end1 - start1)
    if 2 in runs:
        start2 = time.time()
        gifts_ret.append(gifts.iloc[10000:20000])
        gifts_ret[1] = clustering(gifts_ret[1],100)
        gifts_ret[1] = do_trips(100,gifts_ret[1],'run_g2',False,trip_id+500)
        end2 = time.time()
        print(end2 - start2)
    if 3 in runs:
        start3 = time.time()
        gifts3 = gifts.iloc[20000:40000]
        gifts3 = clustering(gifts3,100)
        gifts3 = do_trips(100,gifts3,'run_g3',False,trip_id+1000)
        end3 = time.time()
        print(end3 - start3)
    if 4 in runs:
        gifts4 = gifts.iloc[40000:60000]
        gifts4 = clustering(gifts4,100)
        gifts4 = do_trips(100,gifts4,'run_g4',False,trip_id+1500)
    if 5 in runs:
        start = time.time()
        gifts5 = gifts.iloc[60000:80000]
        gifts5 = clustering(gifts5,100)
        gifts5 = do_trips(100,gifts5,'run_g5',False,trip_id+2000)
    if 6 in runs:
        gifts6 = gifts.iloc[80000:90000]
        gifts7 = gifts.iloc[90000:100000]
        gifts6 = clustering(gifts6,100)
        gifts7 = clustering(gifts7,100)
        gifts6 = do_trips(100,gifts6,'run_g6',False,trip_id+2500)
        gifts7 = do_trips(100,gifts7,'run_g7',False,trip_id+3000)
        end = time.time()
        print(end - start)
    if 10 in runs:
        gifts = clustering(gifts,50)
        gifts = do_trips(50,gifts,'run_it',False,trip_id+4000)
    # for i in gifts_arr:
    #     gifts_ret.append()
    return gifts_ret


# @description: in accordance with the clarke-wright algorithm, we need a savings array
# @param: pandas dataframe
# @output: pandas dataframe with cluster number column
# notes: see your notebook
# ## this might be more of an altered distance function rather than savings



# newfit = newfit.reshape(lat_long.shape)
# plt.figure(1)
# plt.clf()
# plt.imshow(newfit,cmap=plt.cm.Paired, aspect='auto', origin='lower')

def reading_list():
    g1 = pd.read_csv('../data/run_g1.csv')
    g2 = pd.read_csv('../data/run_g2.csv')
    g3 = pd.read_csv('../submissions/run_g3.csv')
    g4 = pd.read_csv('../submissions/run_g4.csv')
    g5 = pd.read_csv('../submissions/run_g5.csv')
    g6 = pd.read_csv('../submissions/run_g6.csv')
    g7 = pd.read_csv('../submissions/run_g7.csv')
    g12 = g1.append(g2)
    g123 = g12.append(g3)
    g1234 = g123.append(g4)
    g12345 = g1234.append(g5)
    g123456 = g12345.append(g6)
    g1_7 = g123456.append(g7)
    g_ord = g1_7.sort(['trip_id','trip_index'], ascending=[True,True])
    null_g = pd.isnull(g_ord.trip_id)
    g_null = g_ord[null_g]
    g_null.set_index('Unnamed: 0')
    null_g2 = pd.isnull(g_null.trip_id)
    g_null2 = g_null[null_g2]
    g_ord3 = g_ord.set_index('Unnamed: 0')
