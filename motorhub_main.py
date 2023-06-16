import re
import time
import requests
from bs4 import BeautifulSoup
import csv
import numpy as np
import pandas as pd

def get_api_params():
    url = "https://www.motorhub.co.ke/all-stock"

    # request the url
    resp = requests.get(url)

    # soup object for data extraction
    soup = BeautifulSoup(resp.text, "lxml")

    # get id
    page_id = soup.find("input", {"type" : "button"}).get("id")

    # csrf code
    csrf_code = re.search(r'csrf_test_name:\"(.*)\"', resp.text).group(1)

    return (page_id, csrf_code)


def get_data(page_id, csrf_code, page_no):
    url = "https://www.motorhub.co.ke/Car/carmore"

    payload = "id={}&csrf_test_name={}&page={}".format(page_id, csrf_code, page_no)
    headers = {
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }

    resp = requests.request("POST", url, headers=headers, data=payload)
    if "No More Cars Found!" in resp.text:
        print("No More Cars Found!\t", page_no)
        return None

    soup = BeautifulSoup(resp.text, "lxml")
    
    car_items = soup.find_all("div", {"class":"card"})

    data = []
    for item in car_items:
        
        # num
        num = item.find("span", {"class":"carNum"}).text
        
        # image
        image = item.find("img").get("src")
        
        # title
        title = item.find("h5", {"class":"display-6"}).text
        
        # price
        price = item.find("h6", {"class":"display-6"}).text
        
        # make year
        make_year = item.find_all("p", {"class":"card-text"})[0].text.replace("Make ", "")

        # engine CC
        engine_cc = item.find_all("p", {"class":"card-text"})[1].text.replace("Engine ", "")

        # availability
        availability = item.find_all("p", {"class":"card-text"})[2].text.replace("Availability ", "")

        # transmission
        transmission = item.find_all("p", {"class":"card-text"})[3].text.replace("Transmission ", "")

        # exterior
        exterior = item.find_all("p", {"class":"card-text"})[4].text.replace("Exterior  ", "")

        # fuel
        fuel = item.find_all("p", {"class":"card-text"})[5].text.replace("Fuel   ", "")

        # drive
        drive = item.find_all("p", {"class":"card-text"})[6].text.replace("Drive    ", "")

        # details link
        details_link = item.find("a", {"class" : "btn btn-primary text-uppercase"}).get("href")

        # reserve link
        reserve_link = item.find("a", {"class" : "btn btn-dark text-uppercase"}).get("href")
        
        data.append((num, image, title, price, make_year, engine_cc, availability, transmission, exterior, fuel, drive, details_link, reserve_link))
    
    return data

# get API params
page_id, csrf_code = get_api_params()

master_data = []
i = 1
while True:
    print("Iteration:\t", i, "\tMaster Data:\t", len(master_data))
    try:
        master_data.extend(get_data(page_id, csrf_code, i+1))
        time.sleep(3)
    except Exception as e:
        print("Error:\t", e)
        break
    i += 1

##with open("motorhub_all_stock.csv", "w") as file:
#    csv_writer = csv.writer(file)
#    csv_writer.writerow(("num", "image", "title", "price", "make_year", "engine_cc", "availability", "transmission", "exterior", "fuel", "drive", "details_link", "reserve_link"))
#    csv_writer.writerows(master_data)

print("File Generated Successfully!!")

## create dataframe
motorhub_df = pd.DataFrame(master_data, columns=["num", "image", "title", "price", "make_year", "engine_cc", "availability", 
                                                 "transmission", "exterior", "fuel", "drive", "details_link", "reserve_link"])


## save dataframe to csv
motorhub_df.to_csv("motorhub_all_stock.csv", index=False)
