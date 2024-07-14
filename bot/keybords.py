from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import WebAppInfo

from config import *

def start_keyboard() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(text="Open WebApp", web_app=WebAppInfo(url=EXCHANGE_URL))

    return builder.as_markup()

