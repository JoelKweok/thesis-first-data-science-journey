
import selenium
from selenium.webdriver import Chrome
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import pandas as pd
import time
import csv
from selenium.common.exceptions import ElementNotInteractableException

webdriver ="C:/Users/User/Downloads/chromedriver_win32/chromedriver.exe"

url = "https://services2.hdb.gov.sg/web/fi10/emap.html"
driver = Chrome(webdriver)
driver.get(url)

time.sleep(14) #to load page
first_postal = "050005"

driver.find_element_by_id("houseIcon").click()
time.sleep(1)
postal_input = driver.find_element_by_id("searchTxt1")
postal_input.send_keys(first_postal) # key in postal code
time.sleep(1)
driver.find_element_by_id("searchButton1").click()
time.sleep(5)
driver.find_element_by_id("sSRRhDT").click() #click on retal rates
time.sleep(2)
num_entry = len(driver.find_elements_by_xpath("/html/body/div[1]/div[2]/section/div[3]/div/div[3]/div/div/fieldset/div[1]/label[6]/div[4]/div/table/tbody"))
#to find length of data entries for the block
total = []

if num_entry == 0:
    new = ("nil","nil","nil",first_postal)
    total.append(new)
else:
    for data in range(1,num_entry+1): #iterate through every row
        string = "//*[@id='sSRRDT']/div/table/tbody[" + str(data) +"]/tr/td[" #getting the xpath locator
        rent_start_month = driver.find_element_by_xpath(string +"1]").get_attribute("innerText") #getting rent start month
        flat_type = driver.find_element_by_xpath(string +"2]").get_attribute("innerText") #getting flat type
        monthly_rent = driver.find_element_by_xpath(string +"3]").get_attribute("innerText") # getting montly rent
        post_code = first_postal
        new = (rent_start_month, flat_type, monthly_rent, first_postal) # compiling entries
        total.append(new)

workbook = pd.read_csv("Desktop/Thesis/data/resale and rental data use this/hdb_data_sqm_final_regression_upgrading.csv")
postal_code = workbook['postal']
    

for x in range(7000,9792):
    error = 0
    postal = str(postal_code[x])
    if(len(postal)<6):
        postal = "0" + postal
    driver.find_element_by_xpath("//*[@id='searchTxt']").clear()
    driver.find_element_by_xpath("//*[@id='searchTxt']").send_keys(postal)
    time.sleep(x%2 +1)
    try:
        driver.find_element_by_id("searchButton").click()
    except:
        try:
            time.sleep(30) #this is for overnight when internet is whacky
            driver.find_element_by_id("searchButton").click()
        except:
            break
    time.sleep(5)
    try:
        driver.find_element_by_id("sSRRhDT").click() #click on retal rates
        time.sleep(3)
    except:
        try:
            time.sleep(10)
            driver.get(url)
            time.sleep(10)
            driver.find_element_by_id("houseIcon").click()
            time.sleep(1)
            postal_input = driver.find_element_by_id("searchTxt1")
            postal_input.send_keys(postal)
            driver.find_element_by_id("searchButton1").click()
            time.sleep(5)
            driver.find_element_by_id("sSRRhDT").click() #click on retal rates
        except:
            error = 1
    if error == 0:
        num_entry = len(driver.find_elements_by_xpath("/html/body/div[1]/div[2]/section/div[3]/div/div[3]/div/div/fieldset/div[1]/label[6]/div[4]/div/table/tbody"))
        if num_entry == 0:
            new = ("nil","nil","nil",postal)
            total.append(new)
        else:
            for data in range(1,num_entry+1): #iterate through every row
                string = "//*[@id='sSRRDT']/div/table/tbody[" + str(data) +"]/tr/td[" #getting the xpath locator
                rent_start_month = driver.find_element_by_xpath(string +"1]").get_attribute("innerText") #getting rent start month
                flat_type = driver.find_element_by_xpath(string +"2]").get_attribute("innerText") #getting flat type
                monthly_rent = driver.find_element_by_xpath(string +"3]").get_attribute("innerText") # getting montly rent
                post_code = postal
                new = (rent_start_month, flat_type, monthly_rent, post_code) # compiling entries
                total.append(new)
    else:
        post_code = postal
        new = ("error", "error" , "error" , post_code)
        total.append(new)

df = pd.DataFrame(total,columns=['rent_start_month','flat_type', 'monthly_rent', 'postal_code'])
df.to_csv('HDB_rent_data_june_7000_9792.csv')

driver.quit()