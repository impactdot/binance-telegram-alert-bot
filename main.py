from aiogram import Bot, Dispatcher, executor, types
from loader import bot, dp, USER_ID

from handler import register_handlers_client
import logging

logging.basicConfig(level=logging.INFO)


async def on_startup(dp):
    await register_handlers_client(dp)


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
    # executor.start_polling(dp, skip_updates=True)
