-- database: cities.db
--что бы код отрабатывал полностью - удаляем таблицы
DROP TABLE IF EXISTS city;

DROP TABLE IF EXISTS district;

DROP TABLE IF EXISTS subject;

-- создаем необходимые таблицы
CREATE TABLE
    IF NOT EXISTS subject (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_name TEXT
    );

CREATE TABLE
    IF NOT EXISTS district (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        district_name TEXT
    );

CREATE TABLE
    IF NOT EXISTS city (
        id INTEGER PRIMARY KEY,
        city_name TEXT,
        lat REAL,
        lon REAL,
        population INTEGER,
        subject_id INTEGER,
        district_id INTEGER,
        FOREIGN KEY (subject_id) REFERENCES subject (id) ON DELETE CASCADE,
        FOREIGN KEY (district_id) REFERENCES district (id) ON DELETE CASCADE
    );

-- создаем индекс
CREATE INDEX IF NOT EXISTS city_name_index ON city (city_name);