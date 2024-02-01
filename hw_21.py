import json
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import requests
from pprint import pprint
from marshmallow import INCLUDE, Schema, fields, ValidationError
from marshmallow_dataclass import class_schema
from marshmallow_jsonschema import JSONSchema
import time
import locale

locale.setlocale(locale.LC_ALL, 'ru_RU')
os.system('cls')


# Загружаем данные с сервера


def get_weather(city_name):
    """
    Получаем данные о погоде по названию города._summary_

    :param city_name: Название города
    :return: JSON с данными о погоде
    """
    api_key = "4d9daf4ee3c722fe353063903d00e608"
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city_name,
        'lang': 'ru',
        'units': 'metric',
        'appid': api_key
    }
    response = requests.get(base_url, params=params)
    return response.json()


# Конвертируем дату в удобочитаемый формат
def get_date_time(date_time: int) -> str:
    """
    Конвертируем дату в удобочитаемый формат

    :param date_time: Дата в формате UNIX
    :return: Дата в удобочитаемом формате в виде строки
    """
    return time.strftime("%d %b %Y %A", time.localtime(date_time))


# Конвертируем время в удобочитаемый формат
def get_shot_date_time(date_time: int) -> str:
    """
    Конвертируем время в удобочитаемый формат

    :param date_time: Дата/время в формате UNIX
    :return: Время в удобочитаемом формате в виде строки
    """
    return time.strftime("%H:%M", time.localtime(date_time))


# Создадим dataclass для хранения данных о погоде для запрошенного города
@dataclass
class CurrentWeather:
    name: str
    dt: int
    weather: List
    main: Dict[str, Any]
    sys: Dict[str, Any]
    base: str
    visibility: int
    timezone: int
    id: int
    cod: int
    coord: Optional[Dict[str, Any]] = None
    wind: Optional[Dict[str, Any]] = None
    clouds: Optional[Dict[str, Any]] = None
    snow: Optional[Dict[str, Any]] = None


# Создаем схему marshmallow для валидации данных
class WeatherSun(Schema):
    sunrise = fields.Int()
    sunset = fields.Int()

    class Meta:
        unknown = INCLUDE


# Создаем схему marshmallow для валидации данных
class WeatherTemp(Schema):
    temp = fields.Float(Required=True)
    feels_like = fields.Float()
    temp_min = fields.Float()
    temp_max = fields.Float()

    class Meta:
        unknown = INCLUDE


# Создаем схему marshmallow для валидации данных
class Weather(Schema):
    description = fields.Str()

    class Meta:
        unknown = INCLUDE


# Создаем схему marshmallow для валидации данных используя marshmallow-dataclass
WeatherSchema = class_schema(CurrentWeather)


# Расширяем базовую схему marshmallow для валидации данных через наследование
class DetailedWeatherSchema(WeatherSchema):
    sys = fields.Nested(WeatherSun)
    main = fields.Nested(WeatherTemp)
    weather = fields.List(fields.Nested(Weather))

    class Meta:
        unknown = INCLUDE


# Создаем расширенную схему
weather_schema = DetailedWeatherSchema()

if __name__ == '__main__':
    # Запрашиваем город для которого будем получать данные о погоде
    weather_data = get_weather(input("Введите город: "))
    try:
        # Валидируем полученные данные
        weather_schema.load(weather_data)
    except ValidationError as e:
        print(e.messages)
    else:
        # Выводим полученные данные
        pprint(f'Погода {get_date_time(weather_data.get("dt"))} в городе {weather_data.get("name")}:')
        pprint(f'Температура: {weather_data.get("main").get("temp")}, {
            weather_data.get("weather")[0].get("description").title()}')
        pprint(f'Температура max: {weather_data.get("main").get("temp_max")}')
        pprint(f'Температура min: {weather_data.get("main").get("temp_min")}')
        pprint(f'Ощущается как: {weather_data.get("main").get("feels_like")}')
        pprint(f'Восход: {get_shot_date_time(weather_data.get("sys").get("sunrise"))}')
        pprint(f'Закат: {get_shot_date_time(weather_data.get("sys").get("sunset"))}')
        # Получаем JSON-схему
        json_schema = JSONSchema().dumps(weather_schema)
        # Если файл JSON-схемы не существует сохраняемм его
        try:
            with open('schema.json', 'r') as file:
                json_schema = json.load(file)
        except FileNotFoundError:
            with open('schema.json', 'w') as file:
                json.dump(json_schema, file, indent=4)
