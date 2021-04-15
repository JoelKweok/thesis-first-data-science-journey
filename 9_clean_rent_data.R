library(tidyverse)
library(readxl)
setwd("C:/Users/User/Desktop/Thesis/data/Rental data")
all_rent = read.csv('all_HDB_rental_June_2019_May_2020.csv', header=T)
HDB_info <- read_excel("hdb_data_complete_excel_file.xlsx")
View(all_rent)
View(HDB_info)

all_rent$`Block` <- NA
all_rent$`Street` <- NA
all_rent$`Max_Floor_Lvl` <- NA
all_rent$`Year_Completed` <- NA
all_rent$`Resi_Tag` <- NA
all_rent$`Comm_Tag` <- NA
all_rent$`Market_Hawker_Tag` <- NA
all_rent$`Gen_Comm_Facil_Tag` <- NA
all_rent$`MS_Carpark_Tag` <- NA
all_rent$`Precint_Pavilion_Tag` <- NA
all_rent$`Town` <- NA
all_rent$`Total_DU` <- NA
all_rent$`No_1_Rm_Sold` <- NA
all_rent$`No_2_Rm_Sold` <- NA
all_rent$`No_3_Rm_Sold` <- NA
all_rent$`No_4_Rm_Sold` <- NA
all_rent$`No_5_Rm_Sold` <- NA
all_rent$`No_Exec_Rm_Sold` <- NA
all_rent$`No_Multigen_Rm_Sold` <- NA
all_rent$`No_Studio_Sold` <- NA
all_rent$`No_1_Rm_Rent` <- NA
all_rent$`No_2_Rm_Rent` <- NA
all_rent$`No_3_Rm_Rent` <- NA
all_rent$`No_Other_Rm_Rent` <- NA

rindex = 0
for(rent_post in all_rent$postal_code){
  rindex = rindex +1
  pindex = 0 
  for(postal in HDB_info$postal){
    pindex = pindex + 1
    if(rent_post == as.numeric(postal)){
      all_rent$`Block`[rindex] <- HDB_info$block[pindex]
      all_rent$`Street`[rindex] <- HDB_info$street[pindex]
      all_rent$`Max_Floor_Lvl`[rindex] <- HDB_info$max_floor_lvl[pindex]
      all_rent$`Year_Completed`[rindex] <- HDB_info$year_completed[pindex]
      all_rent$`Resi_Tag`[rindex] <- HDB_info$residential[pindex]
      all_rent$`Comm_Tag` [rindex] <- HDB_info$commercial[pindex]
      all_rent$`Market_Hawker_Tag`[rindex] <- HDB_info$market_hawker[pindex]
      all_rent$`Gen_Comm_Facil_Tag`[rindex] <- HDB_info$miscellaneous[pindex]
      all_rent$`MS_Carpark_Tag`[rindex] <- HDB_info$multistorey_carpark[pindex]
      all_rent$`Precint_Pavilion_Tag`[rindex] <- HDB_info$precinct_pavilion[pindex]
      all_rent$`Town`[rindex] <- HDB_info$Town[pindex]
      all_rent$`Total_DU`[rindex] <- HDB_info$total_dwelling_units[pindex]
      all_rent$`No_1_Rm_Sold`[rindex] <- HDB_info$X1room_sold[pindex]
      all_rent$`No_2_Rm_Sold`[rindex] <- HDB_info$X2room_sold[pindex]
      all_rent$`No_3_Rm_Sold`[rindex] <- HDB_info$X3room_sold[pindex]
      all_rent$`No_4_Rm_Sold`[rindex] <- HDB_info$X4room_sold[pindex]
      all_rent$`No_5_Rm_Sold` [rindex]<- HDB_info$X5room_sold[pindex]
      all_rent$`No_Exec_Rm_Sold`[rindex] <- HDB_info$exec_sold[pindex]
      all_rent$`No_Multigen_Rm_Sold`[rindex] <- HDB_info$multigen_sold[pindex]
      all_rent$`No_Studio_Sold`[rindex] <- HDB_info$studio_apartment_sold[pindex]
      all_rent$`No_1_Rm_Rent`[rindex] <- HDB_info$X1room_rental[pindex]
      all_rent$`No_2_Rm_Rent`[rindex] <- HDB_info$X2room_rental[pindex]
      all_rent$`No_3_Rm_Rent` [rindex]<- HDB_info$X3room_rental[pindex]
      all_rent$`No_Other_Rm_Rent`[rindex] <- HDB_info$other_room_rental[pindex]
      break
    }
  }
}
View(all_rent)

write.csv(all_rent, file = "rent_hdb_data_final.csv")
