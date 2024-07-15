import asyncio

from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.enums import ParseMode

from . import keybords as kb
from config import *

from app.models import Stock, User, UserStock, Transaction
from app import db, create_app

app = create_app()

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    user_id = int(message.from_user.id)
    with app.app_context():
        if not db.session.query(User).filter_by(user_id_tg=user_id).first():
            user = User(user_id_tg=user_id)
            db.session.add(user)
            db.session.commit()
    
    await message.answer("Hi!\nI'm EchangeCats!\nLet's start.", reply_markup=kb.start_keyboard())


async def run():
    bot = Bot(token=TOKEN_BOT_EXCHANGE, parser_mode=ParseMode.HTML) 
    dp = Dispatcher()
    dp.include_router(router)
    
    print("Bot is running...")

    await bot.delete_webhook(True)
    await dp.start_polling(bot, skip_updates=True)

   