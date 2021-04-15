from onemapsg import OneMapClient
import pandas as pd

Client = OneMapClient("user@gmail.com", "password")
total = []

workbook = pd.read_csv("Desktop/Thesis/data/Proximity data/postal_data.csv")

postal_code = workbook['postal']

# print(postal_code)
# print(Client.search("50004", return_geom=True, get_addr_details=True, page_num=1)['results'][0]['LATITUDE'])

for x in postal_code:
    x = str(x)
    if(len(x)<6):
        x = "0" + x
    lat =  Client.search(x, return_geom=True, get_addr_details=True, page_num=1)['results'][0]['LATITUDE'] #get your lat for start
    longit = Client.search(x, return_geom=True, get_addr_details=True, page_num=1)['results'][0]['LONGITUDE'] #get your long for start
    data = (lat,longit,x)
    total.append(data)

print("done")
df = pd.DataFrame(total,columns=['latitude','longitude', 'postal_code'])
df.to_csv('postal_lat_long.csv')


