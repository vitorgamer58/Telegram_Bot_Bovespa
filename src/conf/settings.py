import os

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
BASE_API_URL = os.getenv("BASE_API_URL")
BISCOINT = os.getenv("BISCOINT_API_URL")
PHOEMUR = os.getenv("FUNDAMENTUS")
COINLIB = os.getenv("COINLIB")
OKANE = os.getenv("OKANE")