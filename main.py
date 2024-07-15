import asyncio
from config import *
from bot import bot
def main():
    asyncio.run(bot.run())

if __name__ == "__main__":
    main()