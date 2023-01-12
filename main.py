from aiogram import executor
from create_bot import dp
from handlers import client

client.register_handlers_client(dp)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
