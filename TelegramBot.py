import requests
import datetime
import time
import os
from dotenv import load_dotenv

load_dotenv()

# Get the bot token from the environment
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def telegram_bot_sendtext(bot_message):

    bot_token=TELEGRAM_BOT_TOKEN
    bot_id=''
    send_text='https://api.telegram.org/bot'+bot_token+'/sendMessage?chat_id='+bot_id+'&text='+bot_message
    response =requests.get(send_text)
    print(datetime.datetime.now().hour)
    for i in range (0,3):
        print(i)
        time.sleep(20)

    return response.json();

telegram_bot_sendtext("Hello Bot")