import asyncio

from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.enums import ParseMode

from . import keybords as kb
from config import *

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    user_id = message.from_user.id
    if not db.check_user(user_id):
        db.add_user(user_id)
    
    await message.answer(f"Hi!\nI'm EchangeCats!\nLet's start., {user_id}")
    #await message.answer("Hi!\nI'm EchangeCats!\nLet's start.", reply_markup=kb.start_keyboard())


async def run():
    bot = Bot(token=TOKEN_BOT_EXCHANGE, parser_mode=ParseMode.HTML) 
    dp = Dispatcher()
    dp.include_router(router)
    
    await bot.delete_webhook(True)
    await dp.start_polling(bot)

    print("Bot is running...")