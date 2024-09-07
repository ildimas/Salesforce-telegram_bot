import os

from aiogram import Bot, types
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("TOKEN")

default_properties = DefaultBotProperties(parse_mode="HTML")

bot = Bot(
    token=TOKEN,
    default=default_properties
)