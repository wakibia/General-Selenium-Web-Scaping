
## load libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import time
import pandas as pd


## website to scrape

website = "https://www.motorhub.co.ke/all-stock"
path = 'C:/Users/cmwak/chrome_driver/chromedriver'

## define a driver variable'
driver = webdriver.Chrome(path)

## open the driver
driver.get(website)

## maximize the window to display all over the screen
driver.maximize_window()

# Click the accept cookies button
accept_button = driver.find_element_by_xpath("//button[text()='Accept']")
accept_button.click()

## get the elements
container = driver.find_element_by_xpath('//div[contains(@class, "row page-content")]')


cars = container.find_elements_by_xpath('.//div[contains(@class, "col-sm-6 col-md-4 col-lg-3")]')



car_name = []
car_price = []
transmission = []
exterior = []
fuel = []
drive = []
engine = []
make = []
car_num = []


for car in cars:
    ## the dot here indicates that the current context is product
    car_name.append(car.find_element_by_xpath('.//h5[contains(@class, "display-6")]').text)
    car_price.append(car.find_element_by_xpath('.//h6[@class = "display-6"]').text)
    transmission.append(car.find_element_by_xpath('.//p[contains(span,"Transmission")]').text)
    exterior.append(car.find_element_by_xpath('.//p[contains(span,"Exterior")]').text)
    fuel.append(car.find_element_by_xpath('.//p[contains(span,"Fuel")]').text)
    drive.append(car.find_element_by_xpath('.//p[contains(span,"Drive")]').text)
    engine.append(car.find_element_by_xpath('.//p[contains(span,"Engine")]').text)
    make.append(car.find_element_by_xpath('.//p[contains(span,"Make")]').text)
    car_num.append(car.find_element_by_xpath('.//span[@class="carNum"]').text)

    ##runtimes.append(product.find_element_by_xpath('.//li[contains(@class,"runtimeLabel")]').text)

## create a dataframe
motorhub_cars = pd.DataFrame(
    {
    "Car_Name" : car_name, "Price": car_price, "Transmission": transmission, \
        "Exterior": exterior, "Fuel": fuel, "Drive": drive, "Engine": engine,
        "Make": make, "Car_Number": car_num
    }
)



## save the dataframe to csv
motorhub_cars.to_csv('motorhub_all_cars.csv', index = False)


print(motorhub_cars)

driver.quit()