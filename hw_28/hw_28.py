"""
TODO

Изучите предоставленную структуру таблиц SQLite.
2. Вам будет предоставлен CSV файл, содержащий данные о карточках приложения.
Столбцы файла включают вопрос, ответ, категорию и теги (с разделителями).
3. Напишите функцию для чтения данных из CSV файла и подготовки структуры данных
для последующей вставки в базу данных.
4. Создайте универсальную функцию для вставки данных с использованием executemany
из библиотеки sqlite3 Python.
5. Реализуйте запросы для записи уникальных тегов в таблицу Tags , используя ранее
созданную функцию.
6. Используйте функцию executemany для записи данных в таблицы Cards и CardTags ,
учитывая структуру связей между таблицами.
7. Напишите функцию поиска, которая позволяет находить карточки по тегу.
8. Реализуйте функцию поиска, которая позволяет находить карточки по вхождению
текста в вопрос или ответ (используя оператор LIKE ).
9. Подготовьте архив, содержащий базу данных SQLite и Python файл с реализованными
функциями.

"""

import json
import sqlite3
import csv
import os
from typing import Dict, List, Set, Union

os.system('cls')

# путь к БД
DB_PATH = 'hw_28.db'
# путь к CSV файлу
# CSV_PATH = 'home_work\hw_28\cards_tags.csv'
CSV_PATH = 'cards_tags.csv'


# функция чтения CSV файл
def get_data_from_csv(file_path: str) -> List[Dict[str, Union[int, str]]]:
    """
    Читает CSV файл
    :param file_path: путь к файлу
    :return: возвращает содержимое файла - values из словаря  
    """
    data_dict = {}
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            card_id = row['CardID']
            category = row['category']
            tags = json.loads(row['tags'])
            # print(row)
            data_dict[card_id] = {'card_id': card_id, 'category': category, 'tags': tags}

    return list(data_dict.values())


# функция получения уникальных значений
def parse_unique_data_by_key(data: List[Dict[str, Union[int, str]]], key: str) -> Set[str]:
    """
    Получение уникальных значений
    :param data: входящий список словарей
    :param key: ключ для поиска
    :return: возвращает set уникальных значений
    """
    tags = []
    for row in data:
        if isinstance(row.get(key), list):
            tags = tags + row.get(key)
        else:
            tags.append(row.get(key))
    # print(tags)
    return set(tags)


# функция выполняет один запрос много раз
def execute_many_queries(cursor: sqlite3.Cursor, query: str, data: list):
    """
    Выполняет один запрос много раз
    :param cursor: курсор
    :param query: запрос
    :param data: данные
    """
    cursor.executemany(query, data)


# функция выполняет полученный SQL запрос и возвращает данные
def fetch_data(query: str, db_path: str):
    """
    Выполняет SQL запрос
    :param query: SQL запрос
    :param db_path: путь к БД
    :return: данные
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()


# функция получения данных по тегам из БД
def get_tags(db_path: str, table_name: str):
    """
    Выполняет SQL запрос
    :param table_name: название таблицы
    :param db_path: путь к БД
    :return: возвращаемые данные
    """
    # формируем SQL запрос
    query = f'''
    SELECT
        *
    FROM
        {table_name};
    '''
    return fetch_data(query, db_path)


# функция поиска карточек по тегу
def search_by_tag(db_path: str, tag: str):
    """
    Выполняет SQL запрос для поиска карточек по тегу
    :param db_path: путь к БД
    :param tag: тег
    :return: возвращаемые данные
    """
    # формируем SQL запрос
    query = f'''
    SELECT * FROM cards c
    LEFT JOIN cardtags ct ON ct.cardid = c.cardid
    WHERE ct.tagid = (select tagid from tags where name='{tag}');
    '''
    return fetch_data(query, db_path)


# функция поиска карточек по тексту в вопросе или ответе
def search_by_text(db_path: str, text: str):
    """
    Выполняет SQL запрос для поиска карточек по тексту
    :param db_path: путь к БД
    :param text: текст
    :return: возвращаемые данные
    """
    # формируем SQL запрос
    query = f'''
    SELECT * FROM cards
    WHERE question LIKE '%{text}%' OR answer LIKE '%{text}%';
    '''
    return fetch_data(query, db_path)


# основная функция запуска
def main():
    # Создаем подключение к БД
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
    # читаем CSV файл
    cards_tags = get_data_from_csv(CSV_PATH)

    # формируем список уникальных значений для тегов
    tags = parse_unique_data_by_key(cards_tags, 'tags')
    tags = [(item,) for item in tags]

    # формируем список уникальных значений для категорий
    categorys = parse_unique_data_by_key(cards_tags, 'category')
    categorys = [(item,) for item in categorys]

    # добавляем данные по тегам в БД
    # query_add_tag = "INSERT INTO tags (name) VALUES (?)"
    # execute_many_queries(cursor, query_add_tag, tags)
    # conn.commit()

    # добавляем данные по категориям в БД
    # query_add_category = "INSERT INTO Categories (name) VALUES (?)"
    # execute_many_queries(cursor, query_add_category, categorys)
    # conn.commit()

    # обновляем данные по категориям в таблицу карточек

    # получаем все данные  из БД и формируем словарь
    categorys_dict_from_db = dict(get_tags(DB_PATH, 'Categories'))
    categorys_list = []
    categoryd_final_data = []

    # формируем список card_id, category
    for item in cards_tags:
        categorys_list.append((item['card_id'], item['category']))
    for item in categorys_list:
        card_id = item[0]
        category_id = [key for key, value in categorys_dict_from_db.items() if value == item[1]]
        categoryd_final_data.append((category_id[0], card_id))

    # обновление СategoryID в таблице карточек
    # query_upd_category = "UPDATE cards SET CategoryID = ? WHERE CardID = ?"
    # execute_many_queries(cursor, query_upd_category, categoryd_final_data)
    # conn.commit()

    # получаем все данные тегов из БД
    tags_dict_from_db = dict(get_tags(DB_PATH, 'tags'))
    tags_list = []
    final_data = []
    # формируем список card_id, category, tag
    for item in cards_tags:
        for tag in item['tags']:
            tags_list.append((item['card_id'], item['category'], tag))
    # формируем итоговый список card_id, tag_id для вставки в БД
    for item in tags_list:
        card_id = item[0]
        tag_id = [key for key, value in tags_dict_from_db.items() if value == item[2]]
        final_data.append((card_id, tag_id[0]))

    # добавляем данные по тегам в сводную таблицу в БД
    # query_add_final_data = "INSERT INTO cardtags (CardID, TagID) VALUES (?, ?)"
    # execute_many_queries(cursor, query_add_final_data, final_data)
    # conn.commit()

    # запускаем поиск по тегу
    get_by_tag = input('Введите тег: ')
    for item in search_by_tag(DB_PATH, get_by_tag):
        print(item)

    # запускаем поиск по тексту вопроса или ответа
    get_by_text = input('Введите текст, который хотите искать: ')
    for item in search_by_text(DB_PATH, get_by_text):
        print(item)


if __name__ == "__main__":
    main()
