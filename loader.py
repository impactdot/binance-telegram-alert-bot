from aiogram import Bot, Dispatcher, executor, types
from decouple import config  # instead of dotenv


API_TOKEN = config("API_TOKEN")
USER_ID = config("USER_ID")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
