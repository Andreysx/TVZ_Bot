import os

import telebot
from telebot import types
from db import create_db
from excel_parser import handle_excel_file
from bot_handlers import handle_search

# BOT_TOKEN = ''
"""Place your telegram bot token"""
bot = telebot.TeleBot(BOT_TOKEN)

ADMIN_IDS = [476525173]
"""Add admin ids"""


# Описать функционал бота.
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """Handles pressing the "Start" button - /start."""
    markup = types.ReplyKeyboardMarkup(row_width=1)
    start_button = types.KeyboardButton('Начать работу')
    markup.add(start_button)
    bot.send_message(message.chat.id, f"Привет {message.from_user.first_name}({message.from_user.username})! "
                                      f"\nНажмите 'Начать работу' для продолжения."
                                      f"\nВы также можете ввести команду id, чтобы узнать свой id в телеграмм",
                     reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Начать работу')
def show_main_menu(message):
    """Displays buttons with basic functionality."""
    markup = types.ReplyKeyboardMarkup(row_width=2)
    btn1 = types.KeyboardButton('Загрузить таблицу Exel')
    btn2 = types.KeyboardButton('Найти товар по артиклу')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Загрузить таблицу Exel')
def prompt_file_upload(message):
    """Handles a click on the "Upload File" button and prompts the user to send the file."""
    if message.from_user.id in ADMIN_IDS:
        bot.send_message(message.chat.id, "Пожалуйста, отправьте мне Excel файл для обработки.")
    else:
        bot.send_message(message.chat.id, "У вас нет прав для загрузки файлов.")


@bot.message_handler(func=lambda message: message.text == 'Найти товар по артиклу')
def prompt_article_search(message):
    """Handles a click on the "Search Article" button and prompts the user to enter the article,
    then passes control to the handle_search function."""
    msg = bot.send_message(message.chat.id, "Введите артикул для поиска:")
    bot.register_next_step_handler(msg, handle_search, bot)



# Парсинг exel файла в дб(squlite) + добавление в дб
@bot.message_handler(content_types=['document'])
def handle_document(message):
    """This function wait for input file and handle him."""
    if message.from_user.id not in ADMIN_IDS:
        # проверка, чтобы только пользователи из списка ADMIN_IDS могли отправить Excel файл
        bot.reply_to(message, "У вас нет прав для загрузки файлов.")
        return

    file_ex = bot.get_file(message.document.file_id)
    file_check = file_ex.file_path.split('.')[-1]

    if file_check not in ['xlsx']:
        # Проверка расширения файла
        bot.reply_to(message, "Пожалуйста, отправьте файл в формате Excel (.xlsx).")
        return

    downloaded_file = bot.download_file(file_ex.file_path)

    final_doc = message.document.file_name

    with open(final_doc, 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.reply_to(message, 'Файл успешно загружен, начинаю обработку...')

    try:
        handle_excel_file(final_doc)
        os.remove(final_doc)
        bot.send_message(message.chat.id, 'Данные успешно загружены в базу данных!')

    except Exception as e:
        bot.reply_to(message.chat.id, f"Произошла ошибка при обработке файла: {e}")


@bot.message_handler()
def info(message):
    """Handle other messages and search telegram id included."""
    if message.text.lower() == 'привет':
        bot.reply_to(message,
                     f'Добрый день, {message.from_user.first_name} {message.from_user.last_name} ({message.from_user.username})')
    elif message.text.lower() == 'id':
        bot.reply_to(message, f' Your ID: {message.from_user.id}')
    elif message.text.lower()[-1] == "?":
        bot.send_message(message.chat.id, f'Я чат бот для работы и не знаю ответа на этот вопрос.')
    else:
        bot.send_message(message.chat.id, f'Я не знаю этой команды. Попробуйте ввести другие команды.')


create_db()

bot.polling(none_stop=True)