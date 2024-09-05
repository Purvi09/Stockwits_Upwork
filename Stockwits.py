import csv
import time
import datetime
from pprint import pprint
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
import pandas as pd
import chromedriver_binary
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
from selenium.webdriver.remote.remote_connection import LOGGER
LOGGER.setLevel(logging.WARNING)

chrome_options = ChromeOptions()

chrome_options.add_argument('window-size=800x841')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument('--no-sandbox')
#chrome_options.add_argument("--headless")
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--lang=en-us")
chrome_options.add_argument("download.default_directory=./")
from dotenv import load_dotenv

prefs = {"profile.password_manager_enabled": False, "credentials_enable_service": False}
chrome_options.add_experimental_option("prefs", prefs)

browser = webdriver.Chrome("bin/chromedriver", options=chrome_options)
time.sleep(5)
load_dotenv()

# Get the username and password from the environment variables
username = os.getenv("STOCKTWITS_USERNAME")
password = os.getenv("STOCKTWITS_PASSWORD")
browser.maximize_window()
count = 0
def login():
    print("Opening Stocktwits")
    browser.get('https://stocktwits.com/signin?next=/')
    time.sleep(5)

    print("Entrying Login Information")
    username_input = browser.find_element(By.NAME,'login')

    username_input.clear()
    username_input.send_keys(username)
    time.sleep(3)
    
    password_input = browser.find_element(By.NAME,'password')

    password_input.clear()
    password_input.send_keys(password)
    time.sleep(3)
    

    login_button = browser.find_element(By.XPATH,"//button[@type='submit']")
    login_button.click()
    time.sleep(10)
    print("Logged In")
    

def post(data, count):
    print("Posting data")
    print(data)

    Post_Button=browser.find_element(By.ID,'sidebar_top_nav_id').find_element(By.TAG_NAME,'button')
    Post_Button.click()

    time.sleep(10)
    text_area=browser.find_elements(By.CLASS_NAME,'DraftEditor-editorContainer')
   
    Span_area=text_area[1].find_element(By.TAG_NAME,'span').send_keys(data)
    time.sleep(5)

    New_Post=browser.find_elements(By.CLASS_NAME,'Default_posting__abipa')[1].find_element(By.TAG_NAME,'button').click()
    time.sleep(10)
   
def main():
    global count
    print(f"{datetime.datetime.now()} Running Main Function")
    curr_day=datetime.datetime.now().weekday()
    curr_hour=datetime.datetime.now().hour
    if(curr_day<5 and curr_hour>=9 and curr_hour< 17):
        
        try:
            df = pd.read_csv("signals.csv", header=None)
            df.columns = ["Tick", "premium", "Strike", "Trade_Type", "Option_Type",  "Expiry", "Size", "Spot", "Price", "PP"]

            f = open("signals.csv", "w")
            f.truncate()
            f.close()

            if(len(df) == 0):
                print("No new signals")
                return
        
            # for index, row in df.iterrows():
            row=df.iloc[-1]
            count = count + 1
            message1=(f'''#WhaleTradeDetected($1M+)   

${row["Tick"]} ${row["Strike"]} {row["Option_Type"]}

 {row["Expiry"]} Exp

Trade Volume: {row["Size"]} Contracts

${row["PP"]} premium paid just now.

Current Stock Price: ${row["Spot"]} 

Trade Type: {row["Trade_Type"]}

Data Source: @EMMOX''' )

            message2=(f'''#WhaleTradeDetected($1M+)   

${row["Tick"]} ${row["Strike"]} {row["Option_Type"]}

 {row["Expiry"]} Exp

Trade Volume: {row["Size"]} Contracts

${row["PP"]} premium paid just now.

Current Stock Price: ${row["Spot"]} 

Trade Type: {row["Trade_Type"]}

Data Source: @EMMOX\n\n''' + "https://www.emmox.com")
        
            if(row["Tick"]!="SPX"):
                if(count<10):
                    post(message1, count)
                else:

                    count=0
                    post(message2,count)

            print("Message posted")
        
        except Exception as e:
            print(e)

    if(curr_day>=5):
        try:
            df = pd.read_csv("recycle.csv", header=None)
            df.columns = ["Tick", "premium", "Strike", "Trade_Type", "Option_Type",  "Expiry", "Size", "Spot", "Price", "PP"]
            for index, row in df.iterrows():
                message1=(f'''#WhaleTradeDetected($1M+)   

${row["Tick"]} ${row["Strike"]} {row["Option_Type"]}

 {row["Expiry"]} Exp

Trade Volume: {row["Size"]} Contracts

${row["PP"]} premium paid just now.

Current Stock Price: ${row["Spot"]} 

Trade Type: {row["Trade_Type"]}

Data Source: @EMMOX''' )
            if(row["Tick"]!="SPX"):
                post(message1, count)

            print("Message posted")
            time.sleep(600)
        
        except Exception as e:
            print(e)


if __name__ == '__main__':
    login()

    while True:
        curr_day=datetime.datetime.now().weekday()
        curr_hour=datetime.datetime.now().hour
        if(curr_day<5 and curr_hour==8):
            f = open("recycle.csv", "w")
            f.truncate()
            f.close()
            time.sleep(1800)
        
        if(curr_day<5 and curr_hour>=9 and curr_hour< 17):
            main()
            time.sleep(300)
        if(curr_day>=5):
            main()
            time.sleep(600)