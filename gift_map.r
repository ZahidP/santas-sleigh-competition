library(spdep)
library(geosphere)
library(threejs)
library(rworldmap)


library(ggplot2)
library(DT)

gifts <- read.csv("../input/gifts.csv")

gifts_coord <- cbind(gifts$Longitude, gifts$Latitude)  # set spatial coordinates
gifts_sp <- SpatialPoints(gifts_coord, proj4string=CRS("+proj=longlat"))
gifts_spdf <- SpatialPointsDataFrame(gifts_sp, data = gifts)
