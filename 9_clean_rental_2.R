library(tidyverse)
library(readxl)
setwd("C:/Users/User/Desktop/Thesis/data/Rental data")
clean_data = read.csv('rent_hdb_data_final.csv', header=T)

clean_data$Region <- NA

index = 0
for(town in clean_data$Town){
  index = 1 +index
  if(town == "SEMBAWANG"|| town == "WOODLANDS" || town == "YISHUN"){
    clean_data$Region[index] <- "North"
  } else if( town == "ANG MO KIO" || town == "HOUGANG" || town == "PUNGGOL" ||town == "SENGKANG" ||town == "SERANGOON"){
    clean_data$Region[index] <- "North-East"
  } else if (town =="BUKIT MERAH"||town =="BISHAN"||town =="BUKIT TIMAH"||town =="CENTRAL AREA"|| town =="GEYLANG"||town =="KALLANG/WHAMPOA"||town =="MARINE PARADE"||town =="QUEENSTOWN"||town =="TOA PAYOH"){
    clean_data$Region[index] <- "Central"
  } else if (town =="BEDOK"||town =="PASIR RIS"||town =="TAMPINES"){
    clean_data$Region[index] <- "East"
  } else if (town =="BUKIT BATOK"||town =="BUKIT PANJANG"||town =="CHOA CHU KANG"||town =="CLEMENTI"|| town =="JURONG EAST"||town =="JURONG WEST"||town =="TENGAH"){
    clean_data$Region[index] <- "West"
  } else {
    clean_data$Region[index] <- "Missing"
  }
}

View(clean_data)
write.csv(clean_data, file = "rent_hdb_data_final_2.csv", row.names = FALSE)

clean_data_2 = read.csv('rent_hdb_data_final_2.csv', header=T)
clean_data_done <- na.omit(clean_data_2)


transform(clean_data_done, monthly_rent = as.numeric(monthly_rent))
transform(clean_data_done, Year_Completed = as.numeric(Year_Completed))
write.csv(clean_data_done, file = "rent_hdb_data_final_remove_NA.csv", row.names = FALSE)