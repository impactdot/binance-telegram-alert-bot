import datetime
import os
from dotenv import load_dotenv

load_dotenv()

print(datetime.datetime.now().strftime("%s"))

print(os.environ["API_TOKEN"])
