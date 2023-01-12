from aiogram import Bot, Dispatcher, executor, types
import requests
from datetime import datetime
from dotenv import load_dotenv
import os
import asyncio

# import logging
# logging.basicConfig(level=logging.INFO)

# loading the .env constants
load_dotenv()
# Constants from .env
API_TOKEN = os.environ["API_TOKEN"]
USER_ID = os.environ["USER_ID"]

# initializing the bot variables required
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


from handlers import client

client.register_handlers_client(dp)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
