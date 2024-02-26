import json
import sqlite3
import os
from pprint import pprint

os.system('cls')

# путь к БД
DB_PATH = 'cities.db'
# путь к SQL скрипту
SQL_SCRIPT_PATH = 'queries.sql'
# путь к JSON файлу
JSON_PATH = 'cities.json'


# функция чтения JSON файл
def read_json(file_path: str):
    """
    Читает JSON файл
    :param file_path: путь к файлу
    :return: возвращает содержимое файла
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


# функция чтения SQL скрипт
def read_sql_queries(file_path: str) -> str:
    """
    Читает SQL скрипт из файла
    :param file_path: путь к файлу
    :return: возвращает содержимое файла
    """
    with open('queries.sql', 'r', encoding='utf-8') as f:
        return f.read()


# функция выполнения SQL скрипта
def execute_sql_script(cursor: sqlite3.Cursor, conn: sqlite3.Connection, sql_script: str):
    """
    Выполняет SQL скрипт
    :param cursor: курсор
    :param sql_script: SQL скрипт
    """
    cursor.executescript(sql_script)
    conn.commit()


# функция выполняет запрос много раз
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


# функция получает название города файла, выполняет по нему SQL запрос и возвращает данные
def get_city_data(city_name: str, db_path: str):
    """
    Выполняет SQL запрос
    :param city_name: название города
    :param db_path: путь к БД
    :return: возвращаемые данные
    """
    # формируем SQL запрос
    query = f'''
    SELECT
        city_name, lat, lon, population, s.name, d.name
    FROM
        city
    JOIN subject s ON city.subject_id = s.subject_id
    JOIN district d ON city.district_id = d.district_id
    WHERE
        {city_name};
    '''
    return fetch_data(query, db_path)


# основная функция запуска
def main():
    # Создаем подключение к БД
    with sqlite3.connect(DB_PATH) as conn:
        # Создаем курсор - это специальный объект, который делает запросы и получает их результаты
        cursor = conn.cursor()

        # Читаем SQL скрипт из файла
        sql_script = read_sql_queries(SQL_SCRIPT_PATH)

        # Выполняем SQL скрипт
        print("Создаем таблицы district, subject и city...")
        execute_sql_script(cursor, conn, sql_script)

    # Заполнение таблиц данными из cities.json
    cities_data = read_json(JSON_PATH)
    subject_name_set = set()
    district_name_set = set()
    cities = []
    for city in cities_data:
        # Формируем список городов
        cities.append(
            (city['name'],
             city['coords']['lat'],
             city['coords']['lon'],
             city['population'],
             city['subject'],
             city['district']))
        # Формируем множества субъектов и районов
        subject_name_set.add(city['subject'])
        district_name_set.add(city['district'])
    # Преобразуем множества в кортежи
    list_of_subject = [(subject,) for subject in subject_name_set]
    list_of_district = [(district,) for district in district_name_set]
    # Заполняем таблицу subject и district данными
    print("Заполняем таблицу subject данными...")
    query_add_subject = "INSERT INTO subject (name) VALUES (?)"
    execute_many_queries(cursor, query_add_subject, list_of_subject)

    print("Заполняем таблицу district данными...")
    query_add_district = "INSERT INTO district (name) VALUES (?)"
    execute_many_queries(cursor, query_add_district, list_of_district)
    conn.commit()

    # Заполняем таблицу city данными из cities.json и id из subject и district
    print("Заполняем таблицу city данными...")
    query_add_city = ("INSERT INTO city (city_name, lat, lon, population, subject_id, district_id) VALUES (?,?,?,?, "
                      "(SELECT subject_id FROM subject WHERE name = ?), (SELECT district_id FROM district WHERE name "
                      "= ?))")
    execute_many_queries(cursor, query_add_city, cities)
    conn.commit()
    conn.close()

    city_input = input('Введите название города или нажмите "Enter", если хотите получить данные по всем городам: ')
    if city_input != '':
        pprint(get_city_data(f'city_name = "{city_input.title()}"', DB_PATH))
    else:
        pprint(get_city_data('city_name NOT NULL', DB_PATH))


if __name__ == "__main__":
    main()
