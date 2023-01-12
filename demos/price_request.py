import requests
import datetime

# Define the start and end dates and times
start_date = "2021-01-01"
start_time = "00:00:00"
end_date = "2021-01-01"
end_time = "00:01:00"

# Convert the dates and times to datetime objects
start_datetime = datetime.datetime.strptime(
    f"{start_date} {start_time}", "%Y-%m-%d %H:%M:%S"
)
end_datetime = datetime.datetime.strptime(f"{end_date} {end_time}", "%Y-%m-%d %H:%M:%S")

# Convert the datetime objects to Unix timestamps in milliseconds
start_timestamp = int(start_datetime.timestamp() * 1000)
end_timestamp = int(end_datetime.timestamp() * 1000)

endpoint = "https://api.binance.com/api/v3/klines"
params = {
    "symbol": "BTCUSDT",
    "interval": "1m",
    "limit": 10,
    "startTime": start_timestamp,
    "endTime": end_timestamp,
}

price_now = requests.get(endpoint, params=params).json()


time_10_min_ago = int(datetime.datetime.now().strftime("%s")) * 1000 - 600000


params = {
    "symbol": "BTCUSDT",
    "interval": "1m",
    "limit": 2,
    "startTime": time_10_min_ago,
    "endTime": time_10_min_ago + 600000,
}

price_now = requests.get(endpoint, params=params).json()

print(price_now)
print(len(price_now))

# response = requests.get(endpoint, params=params)


# if response.status_code == 200:
#     # Request was successful
#     data = response.json()
# else:
#     # Request was unsuccessful
#     data = None


# if data is not None:
#     print(len(data))
