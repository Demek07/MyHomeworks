import pytest
import requests

# Список городов для параметризации тестов
cities = [
    ('Москва', {"lon": 37.6156, "lat": 55.7522}),
    ('Воронеж', {"lon": 39.17, "lat": 51.6664}),
    ('Санкт-Петербург', {"lon": 30.2642, "lat": 59.8944}),
    ('Краснодар', {"lon": 38.9769, "lat": 45.0328}),
    ('Сочи', {"lon": 39.7303, "lat": 43.6}),
]

city_data = [('Москва', {"lon": 37.6156, "lat": 55.7522})]


class WeatherRequest:
    def __init__(self, city_name, expected_coords=None):
        self.city_name = city_name
        self.expected_coords = expected_coords

    def get_weather(self):
        api_key = "4d9daf4ee3c722fe353063903d00e608"
        base_url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': self.city_name,
            'lang': 'ru',
            'units': 'metric',
            'appid': api_key
        }
        response = requests.get(base_url, params=params)
        return response.json()


@pytest.fixture(scope="module")
def weather_request():
    city_name = "Москва"
    expected_coords = {"lon": 37.6156, "lat": 55.7522}
    return WeatherRequest(city_name, expected_coords)


@pytest.fixture()
def weather_request_parametrize(city_name, expected_coords):
    city_name_ = city_name
    expected_coords_ = expected_coords
    return WeatherRequest(city_name_, expected_coords_)


def test_weather_request_city_name(weather_request):
    assert weather_request.city_name == 'Москва', 'В ответе API для Москвы поле name не соответствует ожидаемому (Москва).'


@pytest.mark.parametrize('city_name, expected_coords', city_data)
def test_weather_request_coord(city_name, expected_coords, weather_request):
    assert weather_request.city_name == city_name, "Название города не совпадает"
    assert weather_request.expected_coords['lat'] == expected_coords['lat'], "lon не совпадает"
    assert weather_request.expected_coords['lon'] == expected_coords['lon'], "lat не совпадает"


def test_weather_request_weather_key(weather_request):
    assert 'id' in weather_request.get_weather()['weather'][0], "В данных нет ключа 'id'"
    assert 'main' in weather_request.get_weather()['weather'][0], "В данных нет ключа 'main'"
    assert 'description' in weather_request.get_weather()['weather'][0], "В данных нет ключа 'description'"
    assert 'icon' in weather_request.get_weather()['weather'][0], "В данных нет ключа 'icon'"


def test_weather_request_weather_main_key(weather_request):
    assert 'feels_like' in weather_request.get_weather()['main'], "В данных нет ключа 'feels_like'"
    assert 'temp_min' in weather_request.get_weather()['main'], "В данных нет ключа 'temp_min'"
    assert 'temp_max' in weather_request.get_weather()['main'], "В данных нет ключа 'temp_max'"
    assert 'pressure' in weather_request.get_weather()['main'], "В данных нет ключа 'pressure'"
    assert 'humidity' in weather_request.get_weather()['main'], "В данных нет ключа 'humidity'"


@pytest.mark.slow
@pytest.mark.parametrize('city_name, expected_coords', cities)
def test_weather_request_city_coord_name_parametrize_slow(city_name, expected_coords, weather_request_parametrize):
    assert weather_request_parametrize.city_name == city_name, "Название города не совпадает"
    assert weather_request_parametrize.expected_coords['lon'] == expected_coords['lon'], "lon не совпадает"
    assert weather_request_parametrize.expected_coords['lat'] == expected_coords['lat'], "lat не совпадает"
