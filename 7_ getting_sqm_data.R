setwd("C:/Users/User/Desktop/Thesis/data/Merge rental and resale data")
HDB_facts = read.csv('hdb_data_complete_facts_file.csv', header=T)
sale_data = read.csv('resale 2012 2014.csv', header=T)


#get sqm data from 2012- 2014 
HDB_facts$fa_sqm_1 <- NA
HDB_facts$fa_sqm_2 <- NA
HDB_facts$fa_sqm_3 <- NA
HDB_facts$fa_sqm_4 <- NA
HDB_facts$fa_sqm_5 <- NA
HDB_facts$fa_sqm_exe <- NA
HDB_facts$fa_sqm_mg <- NA
HDB_facts$flat_mod <- NA
HDB_facts$lease_start <- NA

#put postal on 2012-2014 sale data
sale_data$postal <- NA

count_sale = 0
for(sale_st in sale_data$street_name){
  count_sale = count_sale +1
  count_facts = 0
  for(facts_st in HDB_facts$street){
    count_facts = count_facts +1
    if (facts_st == sale_st &&  HDB_facts$block[count_facts] == sale_data$block[count_sale] ){
      sale_data$postal[count_sale] = HDB_facts$postal[count_facts]
      break
    }
  }
}

#put sqm data
sale_count = 0
for(sale_postal in sale_data$postal) {
  hdb_count = 0
  sale_count = sale_count + 1
  for(hdb_postal in HDB_facts$postal){
    hdb_count = hdb_count + 1
    if (sale_postal == hdb_postal && sale_data$flat_type[sale_count] == '1 ROOM'){
      HDB_facts$fa_sqm_1[hdb_count] = sale_data$floor_area_sqm[sale_count]
      #print('1 room')
      break
    } else if(sale_postal == hdb_postal && sale_data$flat_type[sale_count] == '2 ROOM'){
      HDB_facts$fa_sqm_2[hdb_count] = sale_data$floor_area_sqm[sale_count]
      #print('2 room')
      #print(sale_postal)
      break
    } else if(sale_postal == hdb_postal && sale_data$flat_type[sale_count] == '3 ROOM'){
      HDB_facts$fa_sqm_3[hdb_count] = sale_data$floor_area_sqm[sale_count]
      #print('3 room')
      break
    } else if(sale_postal == hdb_postal && sale_data$flat_type[sale_count] == '4 ROOM'){
      HDB_facts$fa_sqm_4[hdb_count] = sale_data$floor_area_sqm[sale_count]
      #print('4 room')
      break
    } else if(sale_postal == hdb_postal && sale_data$flat_type[sale_count] == '5 ROOM'){
      HDB_facts$fa_sqm_5[hdb_count] = sale_data$floor_area_sqm[sale_count]
      #print('5 room')
      break
    } else if(sale_postal == hdb_postal && sale_data$flat_type[sale_count] == 'EXECUTIVE'){
      HDB_facts$fa_sqm_exe[hdb_count] = sale_data$floor_area_sqm[sale_count]
      #print('exe')
      break
    } else if(sale_postal == hdb_postal && sale_data$flat_type[sale_count] == 'MULTI-GENERATION'){
      HDB_facts$fa_sqm_mg[hdb_count] = sale_data$floor_area_sqm[sale_count]
      #print('mg')
      break
    } else{
      
    }
  }
}

#Put in flat model and lease start date from 2012- 2014


hdb_count = 0
for(hdb_postal in HDB_facts$postal) {
  sale_count = 0
  hdb_count = hdb_count + 1
  for(sale_postal in sale_data$postal){
    sale_count = sale_count + 1
    if (sale_postal == hdb_postal){
      HDB_facts$flat_mod[hdb_count] = sale_data$flat_model[sale_count]
      HDB_facts$lease_start[hdb_count] = sale_data$lease_commence_date[sale_count]
      break
    }
  }
}
write.csv(HDB_facts, file = "hdb_data_model_sqm_1.csv")



