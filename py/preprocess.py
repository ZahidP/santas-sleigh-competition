import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
###
from haversine import haversine
from sklearn.cluster import KMeans
from matplotlib import pyplot

# @description: need to caculate distances for cost function
# @param: pandas dataframe
# @output: pandas dataframe with distances
def distances():
    north_pole = (90,0)
    gifts = pd.read_csv('../data/gifts.csv')
    gifts['distance'] = gifts.apply(haver,axis=1)
    gifts['served'] = 0
    gifts['TripId'] = 0
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
    #cax = ax.scatter(lat_long['Longitude'],lat_long['Latitude'], c=labels, cmap=cmhot)
    #plt.show()
    gifts['cluster'] = labels
    return gifts

def run_all():
    gifts = distances()
    gifts1 = gifts.iloc[0:20000]
    gifts2 = gifts.iloc[20000:40000]
    gifts3 = gifts.iloc[40000:60000]
    gifts4 = gifts.iloc[60000:70000]
    gifts5 = gifts.iloc[70000:800000]
    gifts6 = gifts.iloc[80000:90000]
    gifts7 = gifts.iloc[90000:100000]

    gifts1 = clustering(gifts1,100)
    gifts2 = clustering(gifts2,100)
    gifts3 = clustering(gifts3,100)
    gifts4 = clustering(gifts4,100)
    gifts5 = clustering(gifts5,100)
    gifts6 = clustering(gifts6,100)
    gifts7 = clustering(gifts7,100)

    trip_id = 1
    gifts1 = do_trips(100,gifts1,'run_g1',False,trip_id)
    gifts2 = do_trips(100,gifts2,'run_g2',False,trip_id+500)
    gifts3 = do_trips(100,gifts3,'run_g3',False,trip_id+1000)
    gifts4 = do_trips(100,gifts4,'run_g4',False,trip_id+1500)
    gifts5 = do_trips(100,gifts5,'run_g5',False,trip_id+2000)
    gifts6 = do_trips(100,gifts6,'run_g6',False,trip_id+2500)
    gifts7 = do_trips(100,gifts7,'run_g7',False,trip_id+3000)

# @description: in accordance with the clarke-wright algorithm, we need a savings array
# @param: pandas dataframe
# @output: pandas dataframe with cluster number column
# notes: see your notebook
# ## this might be more of an altered distance function rather than savings



# newfit = newfit.reshape(lat_long.shape)
# plt.figure(1)
# plt.clf()
# plt.imshow(newfit,cmap=plt.cm.Paired, aspect='auto', origin='lower')
