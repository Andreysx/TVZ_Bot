import sqlite3
import math

"""This module contains functions to handle messages and commands from users, such as searching by article."""


def handle_search(message, bot):
    """This function handle article request"""
    query = message.text.strip()

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute('SELECT * FROM data WHERE article = ?', (query,))
    result = cur.fetchone()  # Извлекает одну строку из набора результатов

    if result:
        response = f"Артикул: {result[1]}\nНазвание: {result[2]}({result[7]})\nКоличество штук: {result[3]}\n" \
                   f"Цена единицы товара: {round(result[4], 2)} RUB" \
                   f"\nОбщая стоимость: {math.trunc(result[5])} RUB\nВес: {result[6]} кг"
    else:
        response = "Ничего не найдено по данному запросу."

    cur.close()
    conn.close()

    bot.reply_to(message, response)
