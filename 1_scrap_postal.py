import selenium
from selenium.webdriver import Chrome
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium import webdriver #selenium is for webscraping
from selenium.common.exceptions import NoSuchElementException
import pandas as pd 
import time
import csv

webdriver ="C:/Users/User/Downloads/chromedriver_win32/chromedriver.exe"

url = "https://www.singpost.com/find-postal-code"
driver = Chrome(webdriver)
driver.get(url)
postal = []

time.sleep(2) #to load page
first_block = "403"
first_street = "CHOA CHU KANG AVE 3"

block = driver.find_element_by_id("edit-building")
block.send_keys(first_block) # key in block
street = driver.find_element_by_id("edit-street-name")
street.send_keys(first_street) # key in street
act = ActionChains(driver)
act.send_keys(Keys.ENTER).perform()
time.sleep(1)

first_postal = driver.find_element_by_xpath("//*[@id='datatable-1']/tbody/tr/td[1]/p[2]").get_attribute("innerText")
first_row = ("169",first_block,first_street, first_postal)

postal.append(first_row)

workbook = pd.read_csv(r'Desktop/Thesis_documentation/1_Data/hdb_data_complete_postal.csv')

blk = workbook['block']
street_names = workbook['street']

for x in range(450,520):  #as I encountered errors from time to time if I loaded the whole thing, I had to iterate the blocks through batches of 50 - 100
    block_input = blk[x]
    street_input = street_names[x]
    block = driver.find_element_by_id("edit-building")
    time.sleep(x%4 + 2)
    block.clear()
    block.send_keys(block_input) # key in block
    street = driver.find_element_by_id("edit-street-name")
    time.sleep(x%2 + 1)
    street.clear()
    street.send_keys(street_input) # key in street
    act.send_keys(Keys.ENTER).perform()
    time.sleep(x%3 + 1)
    try:
        postal_code = driver.find_element_by_xpath("//*[@id='datatable-1']/tbody/tr/td[1]/p[2]").get_attribute("innerText")
    except NoSuchElementException:
        try:
            time.sleep(10)
            driver.get(url)
            block = driver.find_element_by_id("edit-building")
            block.clear()
            block.send_keys(block_input)
            street = driver.find_element_by_id("edit-street-name")
            street.clear()
            street.send_keys(street_input)
            act.send_keys(Keys.ENTER).perform()
            time.sleep(x%3 + 3)
            postal_code = driver.find_element_by_xpath("//*[@id='datatable-1']/tbody/tr/td[1]/p[2]").get_attribute("innerText")
        except NoSuchElementException: 
            postal_code = "not found"
            break
    data_row = (x,block_input,street_input, postal_code)
    postal.append(data_row)

df = pd.DataFrame(postal,columns=['number','block','street', 'postal'])
df.to_csv('postal_draft_15B.csv')
