from create_bot import bot, dp
from aiogram import types, Dispatcher
import asyncio
from create_bot import background_task


@dp.message_handler(commands=["start"])
async def welcome(message: types.Message):
    await bot.send_message(
        chat_id=message.chat.id,
        text="Hello blyat!\nRun the /percentage command and then /inline command",
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
    # await bot.send_message(query.from_user.id, text=f"Price is {db[-1]}")
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


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(welcome, commands=["start"])
    dp.register_message_handler(inline, commands=["inline"])
    dp.register_callback_query_handler(bitcoin, text="BTCUSDT")
    dp.register_callback_query_handler(ethereum, text="ETHUSDT")
    dp.register_callback_query_handler(xrp, text="XRPUSDT")
    dp.register_callback_query_handler(bnb, text="BNBUSDT")
    dp.register_message_handler(percentage, commands=["percentage"])
    dp.register_callback_query_handler(percent_1, text="1percent")
    dp.register_callback_query_handler(percent_5, text="5percent")
    dp.register_callback_query_handler(percent_10, text="10percent")
