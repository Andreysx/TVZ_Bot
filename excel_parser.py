import pandas as pd
from db import insert_data

"""This module contains functions for parsing Excel files and inserting data into a database."""

def handle_excel_file(file_path):
    """This function handle Excel file and parse him"""
    df = pd.read_excel(file_path)
    # columns = df.iloc[:]
    # df.columns = columns
    # df = df.iloc[:] - Вариант с удаленной шапкой у файла excel
    columns = df.iloc[13, :]
    df = df.iloc[14:, :]
    df.columns = columns

    for _, row in df.iterrows():
        article = str(row.iloc[1])
        name = row.iloc[2]
        quantity = row.iloc[5]
        price_one = row.iloc[6]
        amount = row.iloc[9]
        weight = row.iloc[7]
        eng_name = row.iloc[3]

        insert_data(article, name, quantity, price_one, amount, weight, eng_name)
