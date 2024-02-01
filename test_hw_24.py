import os
import pytest
import requests

# os.system('cls')

cities = [
    ('Москва', {"lon": 37.6156, "lat": 55.7522}),
    ('Воронеж', {"lon": 39.17, "lat": 51.6664}),
    ('Санкт-Петербург', {"lon": 30.2642, "lat": 59.8944}),
    ('Краснодар', {"lon": 38.9769, "lat": 45.0328}),
    ('Сочи', {"lon": 39.7303, "lat": 43.6}),
]

city_data = [('Москва', {"lon": 37.6156, "lat": 55.7522})]


@pytest.fixture
def weather_request_parametrize(city_name):
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


@pytest.fixture
def weather_request(city_name='Москва'):
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


# Номер теста: 1.
def test_weather_request_city_name(weather_request):
    assert weather_request[
               'name'] == 'Москва', 'В ответе API для Москвы поле name не соответствует ожидаемому (Москва).'


# Номер теста: 2.
@pytest.mark.parametrize('city_name, expected_coords', city_data)
def test_weather_request_coord(city_name, expected_coords, weather_request):
    assert weather_request['name'] == city_name, "Название города не совпадает"
    assert weather_request['coord']['lon'] == expected_coords['lon'], "lon не совпадает"
    assert weather_request['coord']['lat'] == expected_coords['lat'], "lat не совпадает"


# Номер теста: 3.
def test_weather_request_weather_key(weather_request):
    assert 'id' in weather_request['weather'][0], "В данных нет ключа 'id'"
    assert 'main' in weather_request['weather'][0], "В данных нет ключа 'main'"
    assert 'description' in weather_request['weather'][0], "В данных нет ключа 'description'"
    assert 'icon' in weather_request['weather'][0], "В данных нет ключа 'icon'"


# Номер теста: 4.
def test_weather_request_weather_main_key(weather_request):
    assert 'feels_like' in weather_request['main'], "В данных нет ключа 'feels_like'"
    assert 'temp_min' in weather_request['main'], "В данных нет ключа 'temp_min'"
    assert 'temp_max' in weather_request['main'], "В данных нет ключа 'temp_max'"
    assert 'pressure' in weather_request['main'], "В данных нет ключа 'pressure'"
    assert 'humidity' in weather_request['main'], "В данных нет ключа 'humidity'"


# Тест 5
# @pytest.mark.slow
@pytest.mark.parametrize('city_name, expected_coords', cities)
def test_weather_request_city_coodrd_name_parametrize_slow(city_name, expected_coords, weather_request_parametrize):
    assert weather_request_parametrize['name'] == city_name, "Название города не совпадает"
    assert weather_request_parametrize['coord']['lon'] == expected_coords['lon'], "lon не совпадает"
    assert weather_request_parametrize['coord']['lat'] == expected_coords['lat'], "lat не совпадает"
