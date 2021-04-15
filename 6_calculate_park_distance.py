import pandas as pd
import time 
import logging
import json
import requests
import geopy as gp
import numpy as np
from geopy.distance import geodesic

workbook = pd.read_csv("Desktop/Thesis/data/For regression/Public housing regression/HDB_regression_rent_west_2_mrt_time.csv")
workbook2 = pd.read_csv("Desktop/Thesis/data/Park data/Postal code of parks in the west.csv")
start = 1
end = 2
HDB_postal_code = workbook['postal']
HDB_lat = workbook['latitude'] 
HDB_long = workbook['longitude'] 
park_name= workbook2['park'] 
park_lat = workbook2['latitude'] 
park_long = workbook2['longitude'] 

list_of_dist_park = []
min_dist = []
for origin in range(0,len(HDB_postal_code)):
    origin_coord = (HDB_lat[origin],HDB_long[origin])
    origin_postal = HDB_postal_code[origin]
    for destin in range(0, len(park_name)):
        destin_coord = (park_lat[destin],park_long[destin])
        destin_name = park_name[destin]
        list_of_dist_park.append(geodesic(origin_coord,destin_coord).meters)
    shortest = (min(list_of_dist_park))
    min_dist.append((shortest,origin_postal))
    print(shortest,origin_postal)
    print(origin)
    list_of_dist_park.clear()

df = pd.DataFrame(min_dist,columns=['nearest_park_ed/m','start']) #put into a dataframe
df.to_csv('public_rent_park_euclidian_dist.csv') #put in excel 
