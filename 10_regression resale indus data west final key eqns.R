library(tidyverse)
library(psych)
library(car)
library(broom)
setwd("C:/Users/User/Desktop/Thesis_documentation/data/For regression/Public housing regression")
resale_data = read.csv('HDB_regression_resale_west_2_aggregate_floors_sensi.csv', header=T)
resale_data_linearity = read.csv('HDB_regression_resale_test_linearity.csv', header =T)

#making factors
resale_data$flat_type.f <- factor(resale_data$flat_type)
resale_data$Town.f <- factor(resale_data$Town)
resale_data$Quarter.f <- factor(resale_data$Quarter)
resale_data$HDB_prog.f <-  factor(resale_data$HDB_prog)
resale_data$storey_range.f <- factor(resale_data$storey_range)


#regression of equation 1 distance##################################
key_vari_price_eqn_1 <- lm(log(price_psm) ~ log(nearest_indus_ed) +  Age + storey_range.f +  flat_type.f  + Town.f + time_to_mrt + nearest_park_ed + Quarter.f, data = resale_data)
summary(key_vari_price_eqn_1)
tidy_eqn1 <- tidy(key_vari_price_eqn_1)
tidy_eqn1
write.csv(tidy_eqn1, "resale_dist_new.csv")
        

#regression of equation 2 dist band 300###################
resale_data$nearest_dist_band_indus_300.f <- factor(resale_data$nearest_dist_band_indus_300)
resale_data$nearest_dist_band_indus_300.f = relevel(resale_data$nearest_dist_band_indus_300.f,ref= 9)
key_vari_price_eqn_2 <- lm(log(price_psm) ~ nearest_dist_band_indus_300.f +  Age + storey_range.f +  flat_type.f  + Town.f + time_to_mrt + nearest_park_ed + Quarter.f, data = resale_data)
summary(key_vari_price_eqn_2)
tidy_eqn2 <- tidy(key_vari_price_eqn_2)
write.csv(tidy_eqn2, "resale_db.csv")


#regression of equation 3 time  ##################
key_vari_price_eqn_3 <- lm(log(price_psm) ~ log(time_to_indus) +  Age + storey_range.f +  flat_type.f  + Town.f + time_to_mrt + nearest_park_ed + Quarter.f, data = resale_data)
summary(key_vari_price_eqn_3)
tidy_eqn3 <- tidy(key_vari_price_eqn_3)
write.csv(tidy_eqn3, "resale_time.csv")

#regression of equation 4 time band 4###################
resale_data$time_band_indus_4.f <- factor(resale_data$time_band_indus_4)
resale_data$time_band_indus_4.f  = relevel(resale_data$time_band_indus_4.f,ref= 7)
key_vari_price_eqn_4 <- lm(log(price_psm) ~ time_band_indus_4.f +  Age + storey_range.f +  flat_type.f  + Town.f + time_to_mrt + nearest_park_ed + Quarter.f, data = resale_data)
summary(key_vari_price_eqn_4)
tidy_eqn4 <- tidy(key_vari_price_eqn_4)
write.csv(tidy_eqn4, "resale_tb.csv")


#normality of errors 

hist(residuals(key_vari_price_eqn_1)) #normality of errors
hist(residuals(key_vari_price_eqn_2)) #normality of errors
hist(residuals(key_vari_price_eqn_3)) #normality of errors
hist(residuals(key_vari_price_eqn_4)) #normality of errors
boxplot(residuals(key_vari_price_eqn_1)) #normality of errors

#linearity test
pairs.panels(resale_data_linearity)
#have to plot x and y invidvidually 

#homoscedasity 
plot(key_vari_price_eqn_1)
plot(key_vari_price_eqn_4)
plot(key_vari_price_eqn_7)
plot(key_vari_price_eqn_9)
     
#multicolinearity 
vif(key_vari_price_eqn_1)
vif_1_price <- tidy(vif(key_vari_price_eqn_1))
write.csv(vif_1_price, "vif_1_price.csv")

vif(key_vari_price_eqn_2)
vif_2_price <- tidy(vif(key_vari_price_eqn_2))
write.csv(vif_2_price, "vif_2_price.csv")

vif(key_vari_price_eqn_3)
vif_3_price <- tidy(vif(key_vari_price_eqn_3))
write.csv(vif_3_price, "vif_3_price.csv")


vif(key_vari_price_eqn_4)
vif_4_price <- tidy(vif(key_vari_price_eqn_4))
write.csv(vif_4_price, "vif_4_price.csv")



#independence of errors 
durbinWatsonTest(key_vari_price_eqn_1)
durbinWatsonTest(key_vari_price_eqn_2)
durbinWatsonTest(key_vari_price_eqn_3)
durbinWatsonTest(key_vari_price_eqn_4)


plot(key_vari_price_eqn_1) #linearity and error distribution