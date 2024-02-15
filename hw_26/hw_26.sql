--1. Создаем таблицу MarvelCharacters
-- CREATE TABLE MarvelCharacters (
--     page_id INTEGER,
--     name TEXT,
--     urlslug TEXT,
--     identify TEXT,
--     ALIGN TEXT,
--     EYE TEXT,
--     HAIR TEXT,
--     SEX TEXT,
--     GSM TEXT,
--     ALIVE TEXT,
--     APPEARANCES INTEGER,
--     FIRST_APPEARANCE TEXT,
--     Year INTEGER
-- );

--2.Создание Новой Таблицы MarvelCharacters_new
CREATE TABLE MarvelCharacters_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    page_id INTEGER,
    name TEXT,
    urlslug TEXT,
    identify TEXT,
    ALIGN TEXT,
    EYE TEXT,
    HAIR TEXT,
    SEX TEXT,
    GSM TEXT,
    ALIVE TEXT,
    APPEARANCES INTEGER,
    FIRST_APPEARANCE TEXT,
    Year INTEGER
);

--3. Цель: Скопировать данные из таблицы MarvelCharacters в MarvelCharacters_new .
INSERT INTO
    MarvelCharacters_new (
        page_id,
        name,
        urlslug,
        identify,
        ALIGN,
        EYE,
        HAIR,
        SEX,
        GSM,
        ALIVE,
        APPEARANCES,
        FIRST_APPEARANCE,
        Year
    )
SELECT
    page_id,
    name,
    urlslug,
    identify,
    ALIGN,
    EYE,
    HAIR,
    SEX,
    GSM,
    ALIVE,
    APPEARANCES,
    FIRST_APPEARANCE,
    Year
FROM
    MarvelCharacters;

DROP TABLE MarvelCharacters;

--4. Переименование Таблицы
ALTER TABLE
    MarvelCharacters_new RENAME TO MarvelCharacters;

--5.Создание Таблиц для Уникальных Значений
CREATE TABLE Sex (
    sex_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
);

CREATE TABLE EyeColor (
    eye_id INTEGER PRIMARY KEY AUTOINCREMENT,
    color TEXT UNIQUE
);

CREATE TABLE HairColor (
    hair_id INTEGER PRIMARY KEY AUTOINCREMENT,
    color TEXT UNIQUE
);

CREATE TABLE Alignment (
    align_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
);

CREATE TABLE LivingStatus (
    status_id INTEGER PRIMARY KEY AUTOINCREMENT,
    status TEXT UNIQUE
);

CREATE TABLE Identity (
    identity_id INTEGER PRIMARY KEY AUTOINCREMENT,
    identity TEXT UNIQUE
);

--6.Наполнение Уникальных Таблиц Данными
INSERT INTO
    Sex (name)
SELECT
    DISTINCT SEX
FROM
    MarvelCharacters;

INSERT INTO
    EyeColor (color)
SELECT
    DISTINCT Eye
FROM
    MarvelCharacters;

INSERT INTO
    HairColor (color)
SELECT
    DISTINCT Hair
FROM
    MarvelCharacters;

INSERT INTO
    Alignment (name)
SELECT
    DISTINCT Align
FROM
    MarvelCharacters;

INSERT INTO
    livingStatus (status)
SELECT
    DISTINCT Alive
FROM
    MarvelCharacters;

INSERT INTO
    Identity (Identity)
SELECT
    DISTINCT identify
FROM
    MarvelCharacters;

--7. Создание Таблицы MarvelCharacters_New с Внешними Ключами
CREATE TABLE MarvelCharacters_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    page_id INTEGER,
    name TEXT,
    urlslug TEXT,
    identity_id INTEGER REFERENCES Identity (identity_id),
    align_id INTEGER REFERENCES Alignment (align_id),
    eye_id INTEGER REFERENCES EyeColor (eye_id),
    hair_id INTEGER REFERENCES HairColor (hair_id),
    sex_id INTEGER REFERENCES Sex (sex_id),
    status_id INTEGER REFERENCES LivingStatus (status_id),
    APPEARANCES INTEGER,
    FIRST_APPEARANCE TEXT,
    Year INTEGER
);

--8.Наполнение Новой Таблицы Данными
INSERT INTO
    MarvelCharacters_New (
        page_id,
        name,
        urlslug,
        identity_id,
        Align_id,
        Eye_id,
        Hair_id,
        Sex_id,
        status_id,
        APPEARANCES,
        FIRST_APPEARANCE,
        Year
    )
SELECT
    m.page_id,
    m.name,
    m.urlslug,
    i.identity_id,
    a.Align_id,
    e.Eye_id,
    h.Hair_id,
    s.Sex_id,
    l.status_id,
    m.APPEARANCES,
    m.FIRST_APPEARANCE,
    m.Year
FROM
    MarvelCharacters m
    LEFT JOIN Alignment a ON m.ALIGN = a.name or (m.ALIGN IS NULL  and a.name IS NULL),
    EyeColor e ON m.EYE = e.color  or ( m.EYE IS NULL and e.color IS NULL),
    HairColor h ON m.HAIR = h.color or (m.HAIR IS NULL and h.color IS NULL),
    Identity i ON m.identify = i.identity or (m.identify IS NULL and i.identity IS NULL),
    LivingStatus l ON m.ALIVE = l.status or (m.ALIVE IS NULL and l.status IS NULL),
    Sex s ON m.SEX = s.name or (m.SEX IS NULL and s.name IS NULL);

--9 Удаление Старой и Переименование Новой Таблицы
DROP TABLE MarvelCharacters;

ALTER TABLE
    MarvelCharacters_new RENAME TO MarvelCharacters;