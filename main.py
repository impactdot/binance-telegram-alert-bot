from aiogram import Bot, Dispatcher, executor, types
from config import API_TOKEN, USER_ID
import requests
from datetime import datetime
from data_storage import price_change_detection
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

url_begin = "https://fapi.binance.com/fapi/v1/trades?symbol="
url_end = "&limit=1"
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
db = []


# can take an argument for a pairing
async def background_task():
    while True:
        await asyncio.sleep(5)
        # print(db)
        # db.append(requests.get(url_begin + "BTCUSDT" + url_end).json()[-1]['price'])
        # заменить этот код на такой: проверять каждые 5 секунд разницу между ценой сейчас и ценой ровно 10 минут назад
        time_now = int(datetime.datetime.now().strftime("%s")) * 1000
        time_10_min_ago = time_now - 600000
        endpoint = "https://api.binance.com/api/v3/klines"
        params = {
            "symbol": "BTCUSDT",
            "interval": "1m",
            "limit": 10,
            "startTime": time_now,
            "endTime": time_now,
        }
        price_now = requests.get(endpoint, params=params).json()[0][1]
        params = {
            "symbol": "BTCUSDT",
            "interval": "1m",
            "limit": 10,
            "startTime": time_10_min_ago,
            "endTime": time_10_min_ago,
        }
        price_10_min_ago = requests.get(endpoint, params=params).json()[0][1]
        if price_now != price_10_min_ago:
            await bot.send_message(
                chat_id=USER_ID,
                text=f"Price changed! {price_10_min_ago} -> {price_now}",
            )


@dp.message_handler(commands=["start"])
async def welcome(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text="Hello blyat!")
    # instead of running it here, we can run it after the user chooses the pairing, a.k.a after /inline command
    await asyncio.create_task(background_task())


# @dp.message_handler(commands='inline')
# async def start_cmd_handler(message: types.Message):
#     keyboard_markup = types.InlineKeyboardMarkup(row_width=3)
#     # default row_width is 3, so here we can omit it actually
#     # kept for clearness

#     text_and_data = (
#         ('BTC-USDT', 'bitcoin'),
#         ('SOL-USD', 'solana'),
#     )
#     # in real life for the callback_data the callback data factory should be used
#     # here the raw string is used for the simplicity
#     row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)

#     keyboard_markup.row(*row_btns)
#     keyboard_markup.add(
#         # url buttons have no callback data
#         types.InlineKeyboardButton('aiogram source', url='https://github.com/aiogram/aiogram'),
#     )

#     await message.reply("NYA", reply_markup=keyboard_markup)


# @dp.callback_query_handler(text='bitcoin')
# async def bitcoin(message: types.Message):
#     while True:
#         if price_change_detection("BTCUSDT", db):
#             await bot.send_message(chat_id=USER_ID, text=f"Price changed! {db[-2]} -> {db[-1]}")
#             await asyncio.sleep(5)


# @dp.callback_query_handler(text='solana')
# async def bitcoin(message: types.Message):
#     while True:
#         if price_change_detection("BTCUSDT", db):
#             await bot.send_message(chat_id=USER_ID, text=f"Price changed! {db[-2]} -> {db[-1]}")
#             await asyncio.sleep(5)


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
    )
    # Send the inline keyboard to the chat
    await bot.send_message(
        message.chat.id,
        "Choose a cryptocurrency pairing:",
        reply_markup=keyboard,
    )


@dp.callback_query_handler(text="BTCUSDT")
async def bitcoin(query: types.CallbackQuery):
    await bot.send_message(query.from_user.id, text=f"Price is {db[-1]}")


@dp.callback_query_handler(text="ETHUSDT")
async def ethereum(query: types.CallbackQuery):
    await bot.send_message(query.from_user.id, text=f"Price is {db[-1]}")


@dp.callback_query_handler(text="XRPCUSDT")
async def xrp(query: types.CallbackQuery):
    await bot.send_message(query.from_user.id, text=f"Price is {db[-1]}")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
