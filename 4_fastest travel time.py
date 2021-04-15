from onemapsg import OneMapClient
import pandas as pd
import time 
import logging

Client = OneMapClient("user@gmail.com", "password") #initiate class 
entry =[]

workbook = pd.read_csv("Desktop/Thesis/data/Private data/broken_private.csv")
workbook2 = pd.read_csv("Desktop/Thesis/data/Proximity data/Industrial area data.csv")
industrial_postal= workbook2['Postal'] 
industrial_zone = workbook2['Zone'] 
hdb_town = workbook['Town']
hdb_postal_code = workbook['postal'][1:20]
hdb_index = 1
indust_index= 0
success = 0
missing =[]
entries = 0

for postal in hdb_postal_code:
    entries += 1
    print("entry " + str(entries))
    indus_time = []
    best_time = 10000
    best_dist = 0
    best_indus = "nil"
    postal = str(postal)
    broken = 0
    indust_index= 0
    best_zone = "NA"
    success = 0
    print(postal)
    if(len(postal)<6):
        postal = "0" + postal    
    start_location = postal
    start_lat = Client.search(start_location, return_geom=True, get_addr_details=True, page_num=1)['results'][0]['LATITUDE'] #get your lat for start
    start_long = Client.search(start_location, return_geom=True, get_addr_details=True, page_num=1)['results'][0]['LONGITUDE'] #get your long for start
    if hdb_town[hdb_index] == "JURONG WEST":
        zones_to_match = ["A", "B", "C", "H"]
    elif hdb_town[hdb_index] == "BUKIT PANJANG":
        zones_to_match = ["J","G"]
    elif hdb_town[hdb_index] == "JURONG EAST":
        zones_to_match = ["B","C","D","G","E"]
    elif hdb_town[hdb_index] == "CLEMENTI":
        zones_to_match = ["E", "F", "G"]
    elif hdb_town[hdb_index] == "BUKIT BATOK":
        zones_to_match = ["B", "J", "H", "G"]
    elif hdb_town[hdb_index] == "CHOA CHU KANG":
        zones_to_match = ["J", "H", "G"]
    else:
        zones_to_match = "error"
    print(hdb_town[hdb_index])
    hdb_index += 1
    print(zones_to_match)
    for indus in industrial_postal:
        #print("indsutrial postal " + str(indus))
        success = 0
        for zone in zones_to_match:
            #print(zone)
            #print(industrial_zone[indust_index])
            #print(indust_index)
            if zone == industrial_zone[indust_index]:
                success = 1
                target_zone = zone
                print("success " + industrial_zone[indust_index])
                break
        indust_index += 1 
        if success  == 0:
            skip_index = indust_index - 1
            hdb_skip_index = hdb_index -1
            print("skip zone " + industrial_zone[skip_index] + " " + postal + " " + hdb_town[hdb_skip_index])
        else:
            end_location = indus
            try:
                end_lat = Client.search(end_location, return_geom=True, get_addr_details=True, page_num=1)['results'][0]['LATITUDE'] #get your lat for end
                end_long = Client.search(end_location, return_geom=True, get_addr_details=True, page_num=1)['results'][0]['LONGITUDE'] #get your long for end
                print("# " + str(entries) + " " + postal + " to " + indus + " trial")
                sum_distance = 0
                travel_login= Client.get_public_transport_route([start_lat,start_long], [end_lat,end_long], '2020-07-13', '07:30:00', 'TRANSIT', max_walk_distance=None, num_itineraries=1) #Travel log of all itinearies. Will always return 3 itinearies
                travel_log = travel_login['plan']['itineraries'][0]
                #print("pass through travel_log 1")
                #print(start_lat,start_long)
                #print(end_lat,end_long)
                for leg_items in travel_log['legs']: #get your total distance
                    sum_distance += leg_items['distance']
                #print("dist1 " + postal + " " + str(sum_distance))
                time_seconds = travel_log['duration'] #get your total time
                time_minutes = round(time_seconds/60,1) #rounding your time
                clean_dist = round(sum_distance) #rounding your distance
                indus_time.append((indus,time_minutes,clean_dist,target_zone))
                print( postal + " to " + indus + "success")
            except Exception:
                try: 
                    time.sleep(80)
                    Client = OneMapClient("reitmo2020@gmail.com", "ssgp5596")
                    print("refreshed")
                    end_lat = Client.search(end_location, return_geom=True, get_addr_details=True, page_num=1)['results'][0]['LATITUDE'] #get your lat for end
                    end_long = Client.search(end_location, return_geom=True, get_addr_details=True, page_num=1)['results'][0]['LONGITUDE'] #get your long for end
                    print("# " + str(entries) + " " + postal + " to " + indus + " trial")
                    sum_distance = 0
                    travel_login= Client.get_public_transport_route([start_lat,start_long], [end_lat,end_long], '2020-07-13', '07:30:00', 'TRANSIT', max_walk_distance=None, num_itineraries=1) #Travel log of all itinearies. Will always return 3 itinearies
                    travel_log = travel_login['plan']['itineraries'][0]
                    #print("pass through travel_log 2")
                    for leg_items in travel_log['legs']: #get your total distance
                        sum_distance += leg_items['distance']
                    time_seconds = travel_log['duration'] #get your total time
                    time_minutes = round(time_seconds/60,1) #rounding your time
                    clean_dist = round(sum_distance) #rounding your distance
                    indus_time.append((indus,time_minutes,clean_dist,target_zone))
                    print( postal + " to " + indus + "success")
                except Exception:
                    missing.append(postal)
                    print("missing" + postal)
                    broken = 1
                    break
    if(broken ==1):
        print("broken " + postal)
        entry.append((start_location,"broken","broken","broken","broken"))
    else:
        #print("not broken " + postal)                     
        for indus_log in indus_time:
            if indus_log[1]<  best_time:
                best_time = indus_log[1]
                best_indus =  indus_log[0]
                best_dist =  indus_log[2]
                best_zone = indus_log[3]
        entry.append((start_location,best_indus,best_time,best_dist,best_zone)) #putting it into your list
        #print("good entry")


df = pd.DataFrame(entry,columns=['start','end','time/min','dist/m', 'zone']) #put into a dataframe
df.to_csv('Travel_time_Indus_1.csv') #put in excel 
