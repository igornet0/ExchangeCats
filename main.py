import mysql.connector
from mysql.connector import errorcode

import asyncio
from . import bot

def main():
    asyncio.run(bot.run())

if __name__ == "__main__":
    main()