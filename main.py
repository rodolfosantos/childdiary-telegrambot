import os
import json
import asyncio
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
import telegram

CD_EMAIL = os.getenv("CD_EMAIL")
CD_PASSWORD = os.getenv("CD_PASSWORD")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


async def main():
    try:
        # Login
        payload = {
            "Username": CD_EMAIL,
            "Password": CD_PASSWORD,
            "RememberMe": True
        }
        headers = {"content-type": "application/json;charset=UTF-8"}

        with requests.Session() as session:
            response = session.post(
                "https://app.childdiary.net/api/Account/login",
                headers=headers,
                data=json.dumps(payload),
            )
            response.raise_for_status()

            # Get Entries
            headers1 = {
                "accept": "application/json, text/plain, */*",
                "cookie": response.headers["Set-Cookie"],
            }

            while True:
                response1 = session.get(
                    "https://app.childdiary.net/api/Entries?count=1&page=0&type=All",
                    headers=headers1,
                )
                response1.raise_for_status()
                responseJSON1 = response1.json()

                createdOn = responseJSON1["Entries"][0]["CreatedOn"]
                createdOnDateTime = datetime.strptime(
                    createdOn, "%Y-%m-%dT%H:%M:%S.%fZ"
                )

                current_datetime = datetime.now()
                oneOurAgo = current_datetime - timedelta(hours=1)

                # Check if the given datetime is greater than one hour ago
                if createdOnDateTime < oneOurAgo:
                    print("No new entries")
                    print("Sleeping for 1 hour")
                    await asyncio.sleep(3600)
                    continue

                # Publish to Telegram
                bot = telegram.Bot(TELEGRAM_TOKEN)
                async with bot:
                    for entry in responseJSON1["Entries"]:
                        print("New entry found, publishing to Telegram!")

                        htmlText = BeautifulSoup(
                            entry["Text"], features="html.parser"
                        )
                        for media in entry["Medias"]:
                            await bot.send_photo(TELEGRAM_CHAT_ID, media["Url"])

                        message = f"{entry['Creator']['Description']}: {htmlText.get_text()}"
                        await bot.sendMessage(TELEGRAM_CHAT_ID, message)

                await asyncio.sleep(3600)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())
