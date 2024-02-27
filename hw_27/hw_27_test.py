import pytest
import sqlite3

# Параметры подключения к базе данных
DB_PATH = 'cities.db'

# Список тестовых данных
test_data = [
    {"city_name": "Абинск", "lat": 44.86667, "lon": 38.16667, "population": 39186, "district": "Южный",
     "subject": "Краснодарский край"},
    {"city_name": "Алзамай", "lat": 55.55, "lon": 98.66667, "population": 5693, "district": "Сибирский",
     "subject": "Иркутская область"},
    {"city_name": "Алупка", "lat": 44.41972, "lon": 34.04306, "population": 8087, "district": "Южный",
     "subject": "Крым"},
    # ... Другие города ...
]


# Функция для подключения к базе данных
def db_connect(db_path):
    conn = sqlite3.connect(db_path)
    return conn


# Тест наличия таблиц
@pytest.mark.parametrize("table_name", ["city", "subject", "district"])
def test_table_exists(table_name):
    """
    Проверка наличия таблицы в базе данных
    sqlite_master - системная таблица, которая содержит информацию о всех таблицах в базе данных
    type='table' - фильтр по типу (table - таблица, index - индекс, trigger - триггер)
    name='{table_name}' - фильтр по имени таблицы
    :param table_name:
    :return:
    """
    conn = db_connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
    assert cursor.fetchone() is not None, f"Таблица {table_name} не найдена"
    conn.close()


# Тест наличия полей в таблице city
@pytest.mark.parametrize("column", ["id", "city_name", "lat", "lon", "population", "subject_id", "district_id"])
def test_city_table_columns(column):
    """
    Проверка наличия поля в таблице city
    PRAGMA table_info(city) - запрос, который возвращает информацию о таблице city

    :param column:
    :return:
    """
    conn = db_connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info(city);")
    columns = [info[1] for info in cursor.fetchall()]
    assert column in columns, f"Поле {column} не найдено в таблице city"
    conn.close()


# Параметризованный тест соответствия данных о городах
@pytest.mark.parametrize("city", test_data)
def test_city_data(city):
    """
    Проверка соответствия данных о городах

    :param city:
    :return:
    """
    conn = db_connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f'''
        SELECT city.city_name, city.lat, city.lon, city.population, subject.subject_name, district.district_name 
        FROM city 
        JOIN subject ON city.subject_id = subject.id 
        JOIN district ON city.district_id = district.id 
        WHERE city.city_name = '{city["city_name"]}'
    ''')
    result = cursor.fetchone()
    assert result is not None, f"Город {city['city_name']} не найден в базе данных"
    assert result[0] == city["city_name"], f"Название города {result[0]} не соответствует ожидаемому {city['city_name']}"
    assert result[1] == city["lat"], f"Широта города {result[1]} не соответствует ожидаемой {city['lat']}"
    assert result[2] == city["lon"], f"Долгота города {result[2]} не соответствует ожидаемой {city['lon']}"
    assert result[3] == city["population"], f"Население города {result[3]} не соответствует ожидаемому {city['population']}"
    assert result[4] == city["subject"], f"Название субъекта {result[4]} не соответствует ожидаемому {city['subject']}"
    assert result[5] == city["district"], f"Название района {result[5]} не соответствует ожидаемому {city['district']}"
    conn.close()
