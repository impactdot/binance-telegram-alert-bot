import requests
import datetime

# Define the start and end dates and times
start_date = "2021-01-01"
start_time = "00:00:00"
end_date = "2021-01-01"
end_time = "00:01:00"

# Convert the dates and times to datetime objects
start_datetime = datetime.datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M:%S")
end_datetime = datetime.datetime.strptime(f"{end_date} {end_time}", "%Y-%m-%d %H:%M:%S")

# Convert the datetime objects to Unix timestamps in milliseconds
start_timestamp = int(start_datetime.timestamp() * 1000)
end_timestamp = int(end_datetime.timestamp() * 1000)

# Print the timestamps
print(start_timestamp)
print(end_timestamp)

endpoint = "https://api.binance.com/api/v3/klines"

params = {
    "symbol": "BTCUSDT",
    "interval": "1m",
    "limit": 10,
    "startTime": 1609459200000,
    # "endTime": 1609462800000,
    "endTime": 1609459200000,
}

response = requests.get(endpoint, params=params)


if response.status_code == 200:
    # Request was successful
    data = response.json()
else:
    # Request was unsuccessful
    data = None


if data is not None:
    print(len(data))