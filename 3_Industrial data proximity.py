import pandas as pd
import time 
import logging
import json
import requests
import geopy as gp
import numpy as np
from geopy.distance import geodesic

workbook = pd.read_csv("Desktop/Thesis/data/For regression/HDB_regression_resale_west_2_aggregate_floors.csv")
workbook2 = pd.read_csv("Desktop/Thesis/data/Proximity data/Industrial area data.csv")
start = 1
end = 2
private_postal_code = workbook['postal']
private_lat = workbook['latitude'] 
private_long = workbook['longitude'] 
industrial_postal= workbook2['postal'] 
industrial_lat = workbook2['latitude'] 
industrial_long = workbook2['longitude'] 

list_of_dist_indus = []
min_dist = []
for origin in range(0,len(private_postal_code)):
    origin_coord = (private_lat[origin],private_long[origin])
    origin_postal = private_postal_code[origin]
    for destin in range(0, len(industrial_postal)):
        destin_coord = (industrial_lat[destin],industrial_long[destin])
        destin_postal = industrial_postal[destin]
        list_of_dist_indus.append(geodesic(origin_coord,destin_coord).meters)
    shortest = (min(list_of_dist_indus))
    min_dist.append((shortest,origin_postal))
    print(shortest,origin_postal)
    print(origin)
    list_of_dist_indus.clear()

df = pd.DataFrame(min_dist,columns=['nearest_indus_ed/m','start']) #put into a dataframe
df.to_csv('public_resale_indus_euclidian_dist.csv') #put in excel 
