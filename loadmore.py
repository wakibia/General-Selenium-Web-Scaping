## import library
## load libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
## scrape data after load more
website = "https://www.motorhub.co.ke/all-stock"
path = 'C:/Users/cmwak/chrome_driver/chromedriver'

## define a driver variable'
driver = webdriver.Chrome(path)

## open the driver
driver.get(website)

## maximize the window to display all over the screen
driver.maximize_window()


## click load more button

## WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.global-modal__dismiss"))).click()
try:
  driver.execute_script("arguments[0].scrollIntoView();", WebDriverWait(driver, 20)).until(EC.element_to_be_clickable((By.XPATH, '//button[@class = "pn-modal__close"]'))).click()
except:
  pass

time.sleep(5)
for i in range(5):
  driver.execute_script("arguments[0].scrollIntoView();", WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button.options__load-more"))))
  WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.options__load-more"))).click()
  print("Load more stories clicked")



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
