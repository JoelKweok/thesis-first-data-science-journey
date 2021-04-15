from onemapsg import OneMapClient

import pandas as pd
import time 

Client = OneMapClient("user@gmail.com", "password") #initiate class 
entry =[]

workbook = pd.read_csv("Desktop/Thesis/data/Proximity data/hdb_mrt_data_broken.csv")
workbook2 = pd.read_csv("Desktop/Thesis/data/Proximity data/mrt_data.csv")
#postal_code = [656289,640701,640702,640704,640818,640820,640832,640863,641274,643273]
postal_code = workbook['Postal'][0:20]
mrt_data = workbook2['Mrt'] 
#mrt_data = [628884,628883,628885,628924,627848,627849,627850]
missing = [] 

for postal in postal_code:
    mrt_time = []
    broken = 0
    best_time = 10000
    best_dist = 0
    best_mrt = "nil"
    postal = str(postal)
    if(len(postal)<6):
        postal = "0" + postal    
    start_location = postal
    start_lat = Client.search(start_location, return_geom=True, get_addr_details=True, page_num=1)['results'][0]['LATITUDE'] #get your lat for start
    start_long = Client.search(start_location, return_geom=True, get_addr_details=True, page_num=1)['results'][0]['LONGITUDE'] #get your long for start
    for mrt in mrt_data:
        end_location = mrt
        end_lat = Client.search(end_location, return_geom=True, get_addr_details=True, page_num=1)['results'][0]['LATITUDE'] #get your lat for end
        end_long = Client.search(end_location, return_geom=True, get_addr_details=True, page_num=1)['results'][0]['LONGITUDE'] #get your long for end
        print( postal + " to " + str(mrt))
        sum_distance = 0
        try:
            travel_login= Client.get_public_transport_route([start_lat,start_long], [end_lat,end_long], '2020-07-13', '07:30:00', 'TRANSIT', max_walk_distance=None, num_itineraries=1) #Travel log of all itinearies. Will always return 3 itinearies
            travel_log = travel_login['plan']['itineraries'][0]
            print("pass through travel_log 1")
            for leg_items in travel_log['legs']: #get your total distance
                sum_distance += leg_items['distance']
            print("dist1 " + postal + " " + str(sum_distance))
            time_seconds = travel_log['duration'] #get your total time
            print("time1 " + postal + " " + str(time_seconds))
            time_minutes = round(time_seconds/60,1) #rounding your time
            clean_dist = round(sum_distance) #rounding your distance
            mrt_time.append((mrt,time_minutes,clean_dist))
            print("clean_dist1 " + postal + " " + str(clean_dist))
        except:
            try:
                time.sleep(180)
                Client = OneMapClient("reitmo2020@gmail.com", "ssgp5596")
                print("refreshed")
                travel_login= Client.get_public_transport_route([start_lat,start_long], [end_lat,end_long], '2020-07-13', '07:30:00', 'TRANSIT', max_walk_distance=None, num_itineraries=1) #Travel log of all itinearies. Will always return 3 itinearies
                travel_log = travel_login['plan']['itineraries'][0]
                print("pass through travel_log 2")
                for leg_items in travel_log['legs']: #get your total distance
                    sum_distance += leg_items['distance']
                time_seconds = travel_log['duration'] #get your total time
                time_minutes = round(time_seconds/60,1) #rounding your time
                clean_dist = round(sum_distance) #rounding your distance
                mrt_time.append((mrt,time_minutes,clean_dist))
                print("clean_dist2 " + postal + " " + str(clean_dist))
            except:
                missing.append(postal)
                print("missing" + postal)
                broken = 1
                break
    if(broken ==1):
        print("broken " + postal)
        entry.append((start_location,"broken","broken","broken"))
    else:
        print("not broken " + postal)
        for mrt_log in mrt_time:
            if mrt_log[1]<  best_time:
                best_time = mrt_log[1]
                best_mrt =  mrt_log[0]
                best_dist =  mrt_log[2]
        entry.append((start_location,best_mrt,best_time,best_dist)) #putting it into your list

print("making excel")
df = pd.DataFrame(entry,columns=['start','end','time/min','dist/m']) #put into a dataframe
df.to_csv('HDB_travel_time_mrt_1.csv') #put in excel 

