# DB CONNECT
try:
    db = mysql.connector.connect(
      host="",
      user="",
      passwd="",
      port="",
      database=""
    )
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Что-то не так с вашим именем пользователя или паролем")
    sys.exit()
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("База данных не существует")
    sys.exit()
  else:
    print(err)
    sys.exit()

cursor = db.cursor()

# Создание базы ,если нет.
cursor.execute("CREATE DATABASE IF NOT EXISTS a0549853_td_bd")

# Создание таблицы, если нет.
cursor.execute("CREATE TABLE IF NOT EXISTS user_info (id INT AUTO_INCREMENT PRIMARY KEY, \
sub INT, lang VARCHAR(255), userid INT, login VARCHAR(255), until TEXT)")
db.commit()
# /DB CONNECT

async def query_db_for_user(user_id):
    cursor = await db.cursor(buffered=True)
    await cursor.execute(
            """
            SELECT phone
            FROM tg_table
            WHERE userid = %s
            """,
            (user_id,)
        )
    
    data = await cursor.fetchone()
    return data

@dp.message_handler(content_types=['text'], state=Test.Q2)
async def handle_text(message):
    await bot.send_message(message.chat.id, 'Ожидайте пару секунд. Идёт поиск...')
    user = await query_db_for_user(message.text)
    if user:
        # пользователь существует
    else:
        # пользователя нет
# run long-polling
if __name__ == '__main__':
executor.start_polling(dp, skip_updates=True)