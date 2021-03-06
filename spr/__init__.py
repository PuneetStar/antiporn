from os.path import exists

from aiohttp import ClientSession
from pyrogram import Client
from Python_ARQ import ARQ
from SafoneAPI import SafoneAPI
from alphabet_detector import AlphabetDetector

api = SafoneAPI()
ad = AlphabetDetector()

API_ID = 6
API_HASH = "eb06d4abfb49dc3eeb1aeb98ae0f581e"
ARQ_API_URL = "https://arq.hamker.in"

if exists("config.py"):
    from config import *
else:
    from sample_config import *

session = ClientSession()


arq = ARQ(ARQ_API_URL, ARQ_API_KEY, session)

spr = Client(
    name="spr",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
)
with spr:
    bot = spr.get_me()
    BOT_ID = bot.id
    BOT_USERNAME = bot.username
