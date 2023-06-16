from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

web = "https://twitter.com/TwitterSupport/status/1415364740583395328"
# web = "https://twitter.com/TwitterSupport"
path = 'C:/Users/cmwak/chrome_driver/chromedriver'
driver = webdriver.Chrome(path)
driver.get(web)
driver.maximize_window()

def get_tweet(element):
    try:
        user = element.find_element_by_xpath(".//span[contains(text(), '@')]").text
        text = element.find_element_by_xpath(".//div[@lang]").text
        tweet_data = [user, text]
    except:
        tweet_data = ['user', 'text']
    return tweet_data


user_data = []
text_data = []
tweet_ids = set()
scrolling = True
while scrolling:
    tweets = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.XPATH, "//article[@role='article']")))
    print(len(tweets))
    for tweet in tweets[-15:]:  # you can change this number with the number of tweets in a website || NOTE: ONLY THOSE LOADED IN THE last page will be considered while those from previous page will be forgotten (example: scroll all the way down and then try to find an @username that it's on top --> it won't find it)
        tweet_list = get_tweet(tweet)
        tweet_id = ''.join(tweet_list)
        if tweet_id not in tweet_ids:
            tweet_ids.add(tweet_id)
            user_data.append(tweet_list[0])
            text_data.append(" ".join(tweet_list[1].split()))

    # Get the initial scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(2)
        # Calculate new scroll height and compare it with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        # condition 1
        if new_height == last_height:  # if the new and last height are equal, it means that there isn't any new page to load, so we stop scrolling
            scrolling = False
            break
        # condition 2
        # if len(data) > 60:
        #     scrolling = False
        #     break
        else:
            last_height = new_height
            break


driver.quit()

df_tweets = pd.DataFrame({'user': user_data, 'text': text_data})
df_tweets.to_csv('tweets_pagination.csv', index=False)
print(df_tweets)
