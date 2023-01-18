import asyncio
import json
import requests
from telegram import Bot, Update
from decouple import config
from flask import Flask, request
from aiohttp import FlaskAioHTTP

app = Flask(__name__)
API_TOKEN = config("API_TOKEN")
bot = Bot(f"{API_TOKEN}")


async def get_updates(update, symbol):
    # Get the current price of the cryptocurrency pairing
    url = "https://api.binance.com/api/v3/ticker/price"
    params = {"symbol": symbol}
    response = requests.get(url, params=params)
    data = json.loads(response.text)
    current_price = data["price"]

    # Send the current price to the Telegram user
    bot.send_message(
        chat_id=update.message.chat_id,
        text=f"The current price of {symbol} is {current_price}",
    )


@app.route("/YOUR_TOKEN", methods=["POST"])
async def handle_updates(request: Request):
    # Extract the update data from the request
    update = request.json()
    message = update.get("message")
    new_symbol = message.get("text")

    global current_task
    global current_symbol

    # If the user sent a different symbol than the one currently being tracked
    if current_symbol != new_symbol:
        # Cancel the current task
        if current_task:
            current_task.cancel()
            current_task = None
            current_symbol = None
        current_symbol = new_symbol
    # Schedule the update task

    async def update_task():
        while True:
            try:
                # Get the current price of the cryptocurrency pairing
                url = "https://api.binance.com/api/v3/ticker/price"
                params = {"symbol": current_symbol}
                response = await requests.get(url, params=params)
                data = json.loads(response.text)
                current_price = data["price"]

                # Send the current price to the Telegram user
                bot.send_message(
                    chat_id=update.message.chat_id,
                    text=f"The current price of {current_symbol} is {current_price}",
                )
                await asyncio.sleep(5)
            except asyncio.CancelledError:
                # Handle task cancellation
                break
            except Exception as e:
                # Handle other errors
                print(f"Error: {e}")
                break

    if not current_task:
        current_task = asyncio.create_task(update_task())
        await current_task


async def main():
    await bot.set_webhook(
        "https://binance-telegram-alert-bot.herokuapp.com/" + bot.token
    )
    await bot.start_webhook(f"/{API_TOKEN}", handle_updates)
    FlaskAioHTTP(app)
    app.run(port=8000)


if __name__ == "__main__":
    asyncio.run(main())
