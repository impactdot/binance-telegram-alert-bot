from aiogram import Bot, Dispatcher, executor, types
from config import API_TOKEN, USER_ID
import requests
from datetime import datetime

# from data_storage import price_change_detection
import asyncio

# import logging

# logging.basicConfig(level=logging.INFO)

url_begin = "https://fapi.binance.com/fapi/v1/trades?symbol="
url_end = "&limit=1"
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
db = []


def price_change_detection(price_1, price_2, percentage):
    if abs(price_1 - price_2) / price_1 >= percentage:
        return True
    else:
        return False


# can take an argument for a pairing
# also add time interval and the percentage change
async def background_task(pairing, percentage=0.01, seconds=120):
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
        if price_change_detection(price_10_min_ago, price_now, percentage):
            await bot.send_message(
                chat_id=USER_ID,
                text=f"Price for {pairing} changed! {price_10_min_ago} -> {price_now}",
            )
        else:
            await bot.send_message(
                chat_id=USER_ID,
                text=f"Price for {pairing} didn't change by { percentage * 100 }%, now it is {price_now}",
            )
        await asyncio.sleep(seconds)


@dp.message_handler(commands=["start"])
async def welcome(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text="Hello blyat!")


# Create a command handler to send the inline keyboard
@dp.message_handler(commands="inline")
async def inline(message: types.Message):
    # Create the inline keyboard markup
    keyboard = types.InlineKeyboardMarkup()
    # Add the cryptocurrency pairings to the inline keyboard
    keyboard.add(
        types.InlineKeyboardButton("BTC/USDT", callback_data="BTCUSDT"),
        types.InlineKeyboardButton("ETH/USDT", callback_data="ETHUSDT"),
        types.InlineKeyboardButton("XRP/USDT", callback_data="XRPUSDT"),
        types.InlineKeyboardButton("BNB/USDT", callback_data="BNBUSDT"),
    )
    # Send the inline keyboard to the chat
    await bot.send_message(
        message.chat.id,
        "Choose a cryptocurrency pairing:",
        reply_markup=keyboard,
    )


@dp.callback_query_handler(text="BTCUSDT")
async def bitcoin(query: types.CallbackQuery):
    # await bot.send_message(query.from_user.id, text=f"Price is {db[-1]}")
    await asyncio.create_task(background_task("BTCUSDT"))


@dp.callback_query_handler(text="ETHUSDT")
async def ethereum(query: types.CallbackQuery):
    # await bot.send_message(query.from_user.id, text=f"Price is {db[-1]}")
    await asyncio.create_task(background_task("ETHUSDT"))


@dp.callback_query_handler(text="XRPUSDT")
async def xrp(query: types.CallbackQuery):
    # await bot.send_message(query.from_user.id, text=f"Price is {db[-1]}")
    await asyncio.create_task(background_task("XRPUSDT"))


@dp.callback_query_handler(text="BNBUSDT")
async def bnb(query: types.CallbackQuery):
    # await bot.send_message(query.from_user.id, text=f"Price is {db[-1]}")
    await asyncio.create_task(background_task("BNBUSDT"))


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
