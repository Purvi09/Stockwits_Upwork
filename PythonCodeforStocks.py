import csv
import requests
import json
import time
import os
from dotenv import load_dotenv
import TelegramBot

# Load environment variables from .env file
load_dotenv()

# Get the URL from the environment variable
url = os.getenv("URL")

while True:
    try:        
        current_time = time.time() * 10000000

        querystring = {
            "heartbeat": "300",
            "tt": "{:0.17f}".format(current_time),
            "tr": "33",  
            "uuid": "4d6c4236-e9e0-45e7-afd2-69db637bcf7a",
            "pnsdk": "PubNub-JS-Web/4.36.0 undefined"
        }

        r = requests.get(url, params=querystring)
        data = r.json()
        data = json.loads(data['m'][0]['d'])

        premium = data["premium"]
        Tick = data['symbol']
        Strike = "{:,}".format(data['strike'])
        Trade_Type = data['type']
        Option_Type = data["optionType"]
        Size = data["size"]
        Expiry = data["expiryString"]
        Spot = "{:,}".format(data["spot"])
        Price = data["price"]
        PP = (Price * Size * 100)
        Size = "{:,}".format(Size)
        Price = "{:,}".format(Price)
        PP = "{:,}".format(PP)

        if Option_Type == 'C':
            Option_Type = 'Calls'
        else:
            Option_Type = 'Puts'

        message = (f'''Massive Options Volume Alert   

${Tick} ${Strike} {Option_Type} {Expiry} Exp

Trade Volume: {Size} Contracts

${PP} premium paid just now.

Current Stock Price: ${Spot} 

Trade Type: {Trade_Type}''')

        if premium >= 1000000:
            with open('signals.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([Tick, premium, Strike, Trade_Type, Option_Type, Expiry, Size, Spot, Price, PP])

            with open('recycle.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([Tick, premium, Strike, Trade_Type, Option_Type, Expiry, Size, Spot, Price, PP])

            TelegramBot.telegram_bot_sendtext(message)

    except Exception as e:
        pass
