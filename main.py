import telebot

bot = telebot.TeleBot('7260906472:AAFwC4N3Z1FVUL2pcK5G4RviCLhKYKnJkqI')



# Сделать кнопку старт с приветсвием пользователя по имени

@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, f"Здарова залупа - {message.from_user.first_name}, "
                                      f"{message.from_user.username}")





#
# Сделать кнопку загрузки Exel  файла(Инаойса) в дб
#
#
# Парсинг exel файла в дб(squlite)
# Кнопка поиска по артикулу
# Поиск в дб артикула вбитого пользователем - Выдача информации

#
#
#

# Обработка текста
@bot.message_handler()
def info(message):
    if message.text.lower() == ' привет':
        bot.send_message(message.chat.id, f"Здарова залупа - {message.from_user.first_name}, "
                                          f"{message.from_user.username}")
    elif message.text.lower() == 'id':
        bot.reply_to(message, f' Your ID: {message.from_user.id}')





bot.polling(none_stop=True)