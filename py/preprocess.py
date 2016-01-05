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
    gifts['cluster'] = labels
    return gifts

# @description: in accordance with the clarke-wright algorithm, we need a savings array
# @param: pandas dataframe
# @output: pandas dataframe with cluster number column
# notes: see your notebook
# ## this might be more of an altered distance function rather than savings



# newfit = newfit.reshape(lat_long.shape)
# plt.figure(1)
# plt.clf()
# plt.imshow(newfit,cmap=plt.cm.Paired, aspect='auto', origin='lower')
