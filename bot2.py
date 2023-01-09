import logging
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update, context):
    keyboard = [[InlineKeyboardButton("BTC/USDT", callback_data='BTCUSDT'),
                 InlineKeyboardButton("ETH/USDT", callback_data='ETHUSDT')],

                [InlineKeyboardButton("XRP/USDT", callback_data='XRPUSDT'),
                 InlineKeyboardButton("LTC/USDT", callback_data='LTCUSDT')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please select a cryptocurrency pair:', reply_markup=reply_markup)

def button(update, context):
    query = update.callback_query

    # Get the current price of the selected cryptocurrency pair
    endpoint = "https://api.binance.com/api/v3/ticker/price"
    params = {"symbol": query.data}
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        data = response.json()
        price = data["price"]
        text = f"The current price of {query.data} is {price}"
    else:
        text = "An error occurred."

    query.edit_message_text(text=text)

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

updater = Updater("TOKEN", use_context=True)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(button))
updater.dispatcher.add_error_handler(error)

updater.start_polling()
updater.idle()
