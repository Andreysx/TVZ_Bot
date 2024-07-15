import sqlite3

"""This module contains functions for working with the database: create_db and insert_data."""
# Создание базы данных и таблицы, если их еще нет
def create_db():
    """Creating database with main table (data) if they not exist."""
    connection = sqlite3.connect('database.db')
    cur = connection.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        article TEXT,
        name TEXT,
        quantity INTEGER,
        price_one REAL,
        amount REAL,
        weight REAL,
        eng_name TEXT)

        ''')
    connection.commit()
    cur.close()
    connection.close()


def insert_data(article, name, quantity, price_one, amount, weight, eng_name):
    """Insert data into database."""
    connection = sqlite3.connect('database.db')
    cur = connection.cursor()

    cur.execute('''
                INSERT INTO data (article, name, quantity, price_one, amount, weight, eng_name) VALUES(?,?,?,?,?,?,?)
                ''', (article.strip(), name, quantity, price_one, amount, weight, eng_name))

    connection.commit()
    cur.close()
    connection.close()