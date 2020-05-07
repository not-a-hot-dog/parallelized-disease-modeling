import pandas as pd
import numpy as np

import geopandas as gpd
from shapely.geometry import Point
from haversine import haversine, Unit

# Function to obtain longitudes
def get_longs(long_dist, longitudes):
    long_med = np.median(longitudes)
    longs = np.linspace(0, long_dist, len(longitudes))
    longs += long_med - np.median(longs)*.9
    return longs

# Function to create a coordinate matrix with dimensions (height, length, 2)
def latlongmatrix(height, length):

    # Setting geographical parameters
    northwest = np.array([49.4, -118.5])
    southeast = np.array([24.4, -80.433]) #-80.433 is the SE tip of Florida

    latitudes = np.linspace(northwest[0], southeast[0], height)
    longitudes = np.linspace(northwest[1], southeast[1], length)

    long_dist = np.array([haversine((i, 0), (i, 1), unit=Unit.MILES) for i in latitudes])
    num_long = len(longitudes) / long_dist

    matrix = np.zeros([len(latitudes), len(longitudes), 2])

    for i in range(matrix.shape[0]):
        matrix[i, :, 0] = latitudes[i]
        matrix[i, :, 1] = get_longs(num_long[i], longitudes)

    return matrix


height = 1792 #US north-south distance in miles
length = 2944 #US east-west distance in miles

# Creating 1792 x 2944 square-mile grid of the US
coord_matrix = latlongmatrix(height, length)

# Create new matrix to be used for Geospark processing
geospark_matrix = np.empty((5275648, 4))

for i in range(coord_matrix.shape[0]):
    for j in range(coord_matrix.shape[1]):
        geospark_matrix[i * coord_matrix.shape[1] + j] = (np.append([i, j], coord_matrix[i, j]))

np.savetxt('geospark_matrix.csv', geospark_matrix, header ='row,col,lat,lon', delimiter=',', comments='')