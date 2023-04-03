import requests
import json
import telegram
import asyncio
import time
from bs4 import BeautifulSoup
import os
from datetime import datetime, timedelta

CD_EMAIL = os.environ["CD_EMAIL"]
CD_PASSWORD = os.environ["CD_PASSWORD"]
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


async def main():

  payload = "{\"Username\":\""+CD_EMAIL+"\",\"Password\":\""+CD_PASSWORD+"\",\"RememberMe\":true}"
  headers = {
    'content-type': 'application/json;charset=UTF-8'
  }

  response = requests.request("POST", "https://app.childdiary.net/api/Account/login", headers=headers, data=payload)
  cookie = response.headers['Set-Cookie']

  #Get Entries

  headers1 = {
    'accept': 'application/json, text/plain, */*',
    'cookie': cookie
  }

  while(True):

    response1 = requests.request("GET", "https://app.childdiary.net/api/Entries?count=1&page=0&type=All", headers=headers1, data={})
    responseJSON1 = json.loads(response1.text)

    createdOn = responseJSON1['Entries'][0]['CreatedOn']
    createdOnDateTime = datetime.strptime(createdOn, '%Y-%m-%dT%H:%M:%S.%fZ')

    current_datetime = datetime.now()
    oneOurAgo = current_datetime - timedelta(hours=1)

    # check if the given datetime is greater than one hour ago
    if createdOnDateTime > oneOurAgo:
      print('No new entries')
      print('Sleeping for 1 hour')
      time.sleep(3600)
      continue;

    #publish to telegram
    bot = telegram.Bot(TELEGRAM_TOKEN)
    async with bot:
        for entry in responseJSON1['Entries']:
          print('New entry found, publishing to telegram!')

          htmlText = BeautifulSoup(entry['Text'], features="html.parser")
          for media in entry['Medias']:
              await bot.send_photo(TELEGRAM_CHAT_ID, media['Url'])

          await bot.sendMessage(TELEGRAM_CHAT_ID, entry['Creator']['Description']+': '+ htmlText.get_text())
    
    time.sleep(3600)


if __name__ == '__main__':
    asyncio.run(main())
