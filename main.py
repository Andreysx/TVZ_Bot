import telebot
from telebot import types
import pandas as pd
import os
import sqlite3


BOT_TOKEN = '7260906472:AAFwC4N3Z1FVUL2pcK5G4RviCLhKYKnJkqI'
bot = telebot.TeleBot(BOT_TOKEN)


# Создание базы данных и таблицы, если их еще нет

def create_db():
    connection = sqlite3.connect('database.db')
    cur = connection.cursor()
    cur.execute('''
         CREATE TABLE IF NOT EXISTS data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            article TEXT,
            name TEXT,
            quantity INTEGER,
            price_one REAL,
            amount REAL)
    
        ''')
    connection.commit()
    cur.close()
    connection.close()




# Сделать кнопки на функционал

# Сделать кнопку старт с приветсвием пользователя по имени

@bot.message_handler(commands=['start', 'help'])
def main(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    # btn1 = types.InlineKeyboardButton('Найти товар по артиклу', callback_data='Поиск артикла')
    # btn2 = types.InlineKeyboardButton('Загрузить таблицу Exel', callback_data='Загрузить файл')
    btn1 = types.KeyboardButton('Найти товар по артиклу')
    btn2 = types.KeyboardButton('Загрузить таблицу Exel')
    markup.row(btn1, btn2)
    bot.send_message(message.chat.id, f"Добрый день - {message.from_user.first_name}, "
                                      f"{message.from_user.username}", reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def callback_message(message):
    if message.text == 'Загрузить таблицу Exel':
        bot.send_message(message.chat.id, "Пожалуйста, отправьте мне Excel файл для обработки.")
    elif message.text == 'Найти товар по артиклу':
        respond = bot.send_message(message.chat.id, "Введите артикул для поиска: ")
        bot.register_next_step_handler(respond, handle_search)
    else:
        pass







#
# Сделать кнопку загрузки Exel  файла(Инаойса) в дб
#
#
# Парсинг exel файла в дб(squlite) + добавление в дб
@bot.message_handler(content_types=['document'])
def handle_document(message):
    file_ex = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_ex.file_path)

    final_doc = message.document.file_name

    with open(final_doc, 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.reply_to(message, 'Файл успешно загружен, начинаю обработку...')

    try:
        #Чтение и обработка Excel файла
        df = pd.read_excel(final_doc)
        # columns = df.iloc[:]
        # df.columns = columns
        df = df.iloc[:]
        os.remove(final_doc)

        #Подключение к базе данных

        connection = sqlite3.connect('database.db')
        cur = connection.cursor()


        #Вставка данных из DataFrame в бд

        for _,row in df.iterrows():
            cur.execute('''
            INSERT INTO data (article, name, quatity, price_one, amount) VALUES(?,?,?,?,?)
            ''', row[0], row[2], row[5], row[6], row[9]) ## --- Проблемыы

        connection.commit()
        cur.close()
        connection.close()

        bot.send_message(message, 'Данные успешно загружены в базу данных!')

    except Exception as e:

        bot.reply_to(message, f"Произошла ошибка при обработке файла: {e}")


# Функция для поиска данных по артикулу
def handle_search(message):
    query = message.text.strip()

    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    c.execute('SELECT * FROM data WHERE article = ?', (query,))
    result = c.fetchone()

    if result:
        response = f"Артикул: {result[1]}\nНазвание: {result[2]}\nЦена: {result[3]}"
    else:
        response = "Ничего не найдено по данному запросу."

    conn.close()

    bot.reply_to(message, response)





# создание дб

# Кнопка поиска по артикулу

# Поиск в дб артикула вбитого пользователем - Выдача информации

#
#
#

# Обработка текста Only after main commands
@bot.message_handler()
def info(message):
    if message.text.lower() == 'привет':
        bot.reply_to(message, f'Добрый день, {message.from_user.first_name} {message.from_user.last_name} ({message.from_user.username})')
        # bot.send_message(message.chat.id, f"Здарова залупа - {message.from_user.first_name}, "
        #                                   f"{message.from_user.username}")
    elif message.text.lower() == 'id':
        bot.reply_to(message, f' Your ID: {message.from_user.id}')
    elif message.text.lower()[-1] == "?":
        bot.send_message(message.chat.id, f'Я чат бот для работы и не знаю ответа на этот вопрос')
    else:
        bot.send_message(message.chat.id, f'Я не знаю этой команды. Попробуйте ввести другие команды.')




create_db()

bot.polling(none_stop=True)