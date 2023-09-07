from loader import bot, dp, USER_ID
from aiogram import types, Dispatcher
import asyncio
import pandas as pd
from datetime import datetime
import requests

user_data = {}

df = pd.DataFrame(columns=["timestamp", "open", "high", "low", "close", "volume"])
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")


def price_change_detection(price_1, price_2, percentage):
    if abs(price_1 - price_2) / price_1 >= percentage:
        return True
    else:
        return False


# can take an argument for a pairing
# also add time interval and the percentage change
async def background_task(pairing, percentage=0.01, seconds=5, user_id=USER_ID):
    global user_data
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
        try:
            prices = requests.get(endpoint, params=params).json()
        except Exception as e:
            print(f"Error fetching data from Binance: {e}")
            return
        price_10_min_ago = float(prices[1][1])
        price_now = float(prices[0][1])
        # append each new fetched price to the dataframe as a row
        df = df.append(
            {
                "timestamp": prices[0][0],
                "open": prices[0][1],
                "high": prices[0][2],
                "low": prices[0][3],
                "close": prices[0][4],
                "volume": prices[0][5],
            },
            ignore_index=True,
        )

        print(df)
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
        if user_data.get(user_id, {}).get("stop_task"):
            break


@dp.message_handler(commands=["start"])
async def welcome(message: types.Message):
    await bot.send_message(
        chat_id=message.chat.id,
        text="Hello!\nRun the /percentage command and then /inline command",
    )


# Create a command handler to send the inline keyboard
@dp.message_handler(commands="inline")
async def inline(message: types.Message):
    # Create the inline keyboard markup
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
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
    await bot.send_message(query.from_user.id, text="asfdsasfd")
    global user_data
    # Stop any existing task for this user
    user_data[query.from_user.id] = {"stop_task": True}
    await asyncio.sleep(1)  # Give the task a moment to stop
    user_data[query.from_user.id] = {"stop_task": False}
    await asyncio.create_task(
        background_task("BTCUSDT", percentage=percentage, user_id=query.from_user.id)
    )


@dp.callback_query_handler(text="ETHUSDT")
async def ethereum(query: types.CallbackQuery):
    # await bot.send_message(query.from_user.id, text=f"Price is {db[-1]}")
    await asyncio.create_task(
        background_task("ETHUSDT", percentage=percentage, user_id=query.from_user.id)
    )


@dp.callback_query_handler(text="XRPUSDT")
async def xrp(query: types.CallbackQuery):
    # await bot.send_message(query.from_user.id, text=f"Price is {db[-1]}")
    await bot.send_message(query.from_user.id, text="yooooo")
    await asyncio.create_task(
        background_task("XRPUSDT", percentage=percentage, user_id=query.from_user.id)
    )


@dp.callback_query_handler(text="BNBUSDT")
async def bnb(query: types.CallbackQuery):
    # await bot.send_message(query.from_user.id, text=f"Price is {db[-1]}")
    await asyncio.create_task(
        background_task("BNBUSDT", percentage=percentage, user_id=query.from_user.id)
    )


@dp.message_handler(commands=["percentage"])
async def percentage(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    # Add the cryptocurrency pairings to the inline keyboard
    keyboard.add(
        types.InlineKeyboardButton("1%", callback_data="1percent"),
        types.InlineKeyboardButton("5%", callback_data="5percent"),
        types.InlineKeyboardButton("10%", callback_data="10percent"),
    )
    # Send the inline keyboard to the chat
    await bot.send_message(
        message.chat.id,
        "Choose a percentage",
        reply_markup=keyboard,
    )


@dp.callback_query_handler(text="1percent")
async def percent_1(query: types.CallbackQuery):
    global percentage
    percentage = 0.01
    await bot.send_message(
        chat_id=query.from_user.id, text=f"Percentage is {percentage * 100}%"
    )


@dp.callback_query_handler(text="5percent")
async def percent_5(query: types.CallbackQuery):
    global percentage
    percentage = 0.05
    await bot.send_message(
        chat_id=query.from_user.id, text=f"Percentage is {percentage * 100}%"
    )


@dp.callback_query_handler(text="10percent")
async def percent_10(query: types.CallbackQuery):
    global percentage
    percentage = 0.1
    await bot.send_message(
        chat_id=query.from_user.id, text=f"Percentage is {percentage * 100}%"
    )


async def on_startup(dp: Dispatcher):
    await register_handlers_client(dp)


async def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(welcome, commands=["start"])
    dp.register_message_handler(percentage, commands=["percentage"])
    dp.register_message_handler(inline, commands=["inline"])
    dp.register_callback_query_handler(bitcoin, text="BTCUSDT")
    dp.register_callback_query_handler(ethereum, text="ETHUSDT")
    dp.register_callback_query_handler(xrp, text="XRPUSDT")
    dp.register_callback_query_handler(bnb, text="BNBUSDT")
    dp.register_callback_query_handler(percent_1, text="1percent")
    dp.register_callback_query_handler(percent_5, text="5percent")
    dp.register_callback_query_handler(percent_10, text="10percent")
