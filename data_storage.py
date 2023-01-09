# надо записывать цены, если были изменения, то отправлять сообщение
import requests
import time 
import asyncio

url_begin = "https://fapi.binance.com/fapi/v1/trades?symbol="
url_end = "&limit=1"


def adding_to_db(pairing, db):
    db.append(requests.get(url_begin + pairing + url_end).json()[-1]['price'])



def price_change_detection(pairing, db):
    if (db[-1] != db[-2]):
        print(f"Price changed! {db[-2]} -> {db[-1]}")
        return db[-1]
