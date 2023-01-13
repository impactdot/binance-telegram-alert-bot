from aiogram import Bot, Dispatcher, executor, types
from decouple import config  # instead of dotenv
import os
import requests
from datetime import datetime
import asyncio


# loading the .env constants
API_TOKEN = config("API_TOKEN")
USER_ID = config("USER_ID")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def price_change_detection(price_1, price_2, percentage):
    if abs(price_1 - price_2) / price_1 >= percentage:
        return True
    else:
        return False


# can take an argument for a pairing
# also add time interval and the percentage change
async def background_task(pairing, percentage=0.01, seconds=120, user_id=USER_ID):
    while True:
        time_10_min_ago = int(datetime.now().strftime("%s")) * 1000 - 600000
        endpoint = "https://api.binance.com/api/v3/klines"
        params = {
            "symbol": pairing,
            "interval": "1m",
            "limit": 2,
            "startTime": time_10_min_ago,
            "endTime": time_10_min_ago + 600000,
        }
        # shows two prices, first at time_10_min_ago, second at time_now
        prices = requests.get(endpoint, params=params).json()
        price_10_min_ago = float(prices[1][1])
        price_now = float(prices[0][1])
        # we could change the percentage later
        # заменить bot.send_message на простой возврат значения, а в main.py уже отправлять
        # тогда возможно прийдется передвинуть await async.sleep в другое место
        # return делать нельзя, т.к. тогда мы выйдем из while True:
        # тогда костыль
        if price_change_detection(price_10_min_ago, price_now, percentage):
            await bot.send_message(
                chat_id=user_id,
                text=f"Price for {pairing} changed! {price_10_min_ago} -> {price_now}",
            )
        else:
            await bot.send_message(
                chat_id=user_id,
                text=f"Price for {pairing} didn't change by { percentage * 100 }%, now it is {price_now}",
            )
        await asyncio.sleep(seconds)
