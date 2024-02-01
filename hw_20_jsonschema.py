import json
import random
from dataclasses import dataclass
from prettytable import PrettyTable
from typing import List
from jsonschema import validate, ValidationError

# Загружаем JSON-схему
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "population": {"type": "integer"},
        "subject": {"type": "string"},
        "district": {"type": "string"},
        "latitude": {"type": "number"},
        "longitude": {"type": "number"},
        "is_used": {"type": "boolean"},
        "is_badchar": {"type": "boolean"},
    },
    # Для игры нам нужно обязательно только поле name
    "required": ["name"]
}


class JsonFile:
    """
    Класс JsonFile : класс для работы с JSON.
    read_json: метод для загрузки данных из JSON
    write_json: метод для записи данных в JSON
    """

    # Загружаем данные из JSON (в виде списка)
    def read_json(self, load_file: str) -> set:
        """
        Загрузка списка городов из JSON
        :return: возвращаем список данных
        """
        with open(load_file, "r", encoding="utf-8") as file:
            data_list_set = json.load(file)
        return data_list_set

    # Записываем данные в JSON
    def write_json(self, data: List, save_file: str):
        """
        Запись данных в JSON
        :data: данные для записи в JSON
        :save_file: имя файла для сохранения
        """
        with open(save_file, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)


@dataclass
class City(JsonFile):
    """
    Датаклас для загрузки данных о городах
    :return: состояние об использовании города и список городов с "плохим" символом
    """
    name: str
    population: int
    subject: str
    district: str
    latitude: float
    longitude: float
    is_used: bool = False
    is_badchar: bool = True

    def __post_init__(self):
        self.name = self.name.capitalize()

    def __bool__(self):
        """
        Проверка, был ли использован ли этот город в игре или нет
        и проверка на вхождение в список "плохих букв"
        :return: True если город использован, False если нет
        """
        return self.is_badchar, self.is_used


class Cities(JsonFile):
    """
    Класс Cities : Класс для представления данных о городах из JSON-файла.
    Содержит список всех городов.
    """

    # Функция для получения списка городов
    def get_cities(self):
        """
        Загрузка списка городов из JSON
        :return: возвращаем списки городов
        """
        # Загружаем города из JSON
        # serializer = CitySerializer()
        cities_list_set = []
        cities_data = self.read_json('cities.json')
        # Создаем список городов b и проверяем на валидность данных
        for item in cities_data:
            try:
                validate(instance=item, schema=schema)
                # city = serializer(item)
                cities_list_set.append(City(
                    item["name"],
                    item["population"],
                    item["subject"],
                    item["district"],
                    item["coords"]["lat"],
                    item["coords"]["lon"]
                ))
            except ValidationError as e:
                print(f"Ошибка в данных: {e}")
        # Помечаем города "хорошими буквами" - is_badchar = False
        for city in cities_list_set:
            for city_ in cities_list_set:
                if city.name[-1].lower() == city_.name[0].lower():
                    city.is_badchar = False
                    break

        return cities_list_set


class CityGame(JsonFile):
    """
    Класс CityGame : Класс управления игрой.
    """

    def __init__(self, cities_set):
        """
        Инициализация класса
        """
        self.cities_set = cities_set
        # Признак окончания игры
        self.stop: bool = False
        # Список победителей
        self.winners_list: List = []
        # Последний символ в названии города
        self.last_char: str = ''
        # Шаг игры
        self.step: int = 1
        # Победитель
        self.winner: str = ''
        # Признак - "плохой буквы"
        self.bad_char: bool = True

    def start_game(self):
        """
        Метод для начала игры, который включает первый ход компьютера.
        """
        print("Игра началась!")
        print("Компьютер ходит первым.")

    # Выводим список победителей c проверкой на существование файла победителей
    def print_winners(self):
        """
        Выводим список победителей
        """
        # Пытаемся загрузить список победителей
        try:
            self.winners_list = list(self.read_json('winners.json'))
        # Если файл не существует - создаём пустой список
        except FileNotFoundError:
            self.winners_list = [None, None, None, None, None]
        # Формируем таблицу с победителями с помощью PrettyTable
        winners_table = PrettyTable()
        winners_table.field_names = ["№ п/п", "Победитель"]
        for index in range(len(self.winners_list)):
            winners_table.add_row([index + 1, self.winners_list[index]])
        print('Таблица победителей:')
        print(winners_table)

    def last_char_check(self, city: str) -> bool:
        """
        Проверяем последний символ в названии города
        :param city: Название города
        :return: Bool
        """
        if city[0].lower() == self.last_char.lower():
            return True
        else:
            print(f"Некорректный ввод - город должен начинаться с буквы {self.last_char.upper()}. "
                  f"Попробуйте еще раз.")
            return False

    def is_valid_city(self, city: str) -> bool:
        """
        Проверка вхождения в список "чистых" городв
        :param city: Название города
        :return: Bool
        """
        for city_ in self.cities_set:
            if city_.name.title() == city.title():
                return True
        return False

    def stop_game(self, stop: str):
        """
        Метод для завершения игры
        """
        if stop.lower() == "стоп":
            print(f'Вы остановили игру. Вы проиграли! на {self.step} ходу')
            self.stop = True
            self.winner = 'Компьютер'
            self.save_game_state()
            return True
        else:
            return False

    def included_in_badchar(self, city: str) -> bool:
        """
        Выводим проверку на вхождение в список "плохих букв"
        :param city: название города
        :return: Bool
        """
        for city_ in self.cities_set:
            if city_.name.title() == city.title() and city_.is_badchar:
                print(f'Город {city.title()} в списке \'плохих букв\'. Попробуйте еще раз.')
                self.bad_char = True
                return True
        else:
            self.bad_char = False
            return False

    def upd_cities_list(self, city_name: str):
        """
        Удаление города из списка городов и добавление в список использованных
        :param city_name: название города
        """
        # Помечаем использованный город, что бы не повторялся город
        for city in self.cities_set:
            if city_name.title() == city.name.title():
                city.is_used = True
                break

    def city_used_check(self, city):
        """
        Проверка использовался город в игре или нет
        :param city: Название города
        :return: Bool
        """
        for city_ in self.cities_set:
            if city.title() == city_.name and city_.is_used:
                print(f'Город {city.title()} уже называли. Вы проиграли на {self.step} ходу!')
                return True
        return False

    def human_turn(self, city_input):
        """
        Метод для хода человека, который будет обрабатывать ввод пользователя.
        """
        # Проверяем называли город из списка городов или нет
        if self.city_used_check(city_input.title()):
            self.stop = True
            # Обновляем список победителей
            self.winner = 'Компьютер'
            self.save_game_state()
        # Проверяем вхождение в список "плохих" букв
        # elif self.included_in_badchar(city_input):
        # pass
        # Проверяем существование города
        elif self.is_valid_city(city_input):
            # Обновляем последний символ
            self.last_char = city_input[-1]
            # Выводим сообщение
            print(f'Вы назвали город {city_input.title()}. Компьютеру город на {self.last_char.upper()}')
            # Обновляем списки городов
            self.upd_cities_list(city_input)
            # Делаем шаг
            self.step += 1
        elif not self.is_valid_city(city_input) and not self.bad_char:
            # Города нет ни в списке городов, ни в списке "плохих букв",
            # ни в списке использованных - выводим сообщение
            print(f'Город {city_input.title()} не существует. Вы проиграли на {self.step} ходу!')
            self.stop = True
            # Обновляем список победителей
            self.winner = 'Компьютер'
            self.save_game_state()

    def computer_turn(self):
        """
        Метод для хода компьютера
        """
        # Проверяем последний символ
        if self.last_char != '':
            # Ищем город на последний символ
            for city_comp in self.cities_set:
                if city_comp.name[0].lower() == self.last_char.lower() and (
                        not city_comp.is_used and not city_comp.is_badchar):
                    # Определяем последний символ в названии города
                    self.last_char = city_comp.name[-1]
                    # Выводим сообщение
                    print(f'Компьютер называет город {city_comp.name.title()}. Вам город на {self.last_char.upper()}')
                    # Проверяем и обновляем списки городов
                    self.upd_cities_list(city_comp.name)
                    # Делаем шаг
                    self.step += 1
                    break
            else:
                # Если компьютер не может назвать город - выводим сообщение
                print(f'Компьютер не может назвать город. Вы выиграли на {self.step} ходу!')
                # Обновляем список победителей
                self.winner = 'Пользователь'
                self.save_game_state()
                self.stop = True
        else:
            # Первый ход компьютера - случайно выбираем город
            while True:
                city_comp = random.choice(list(self.cities_set))
                if not city_comp.is_badchar:
                    break
            self.last_char = city_comp.name[-1]
            # Выводим сообщение
            print(f'Компьютер называет город {city_comp.name.title()}. Вам город на {self.last_char.upper()}')
            # Проверяем и обновляем списки городов
            self.upd_cities_list(city_comp.name)
            # Делаем шаг
            self.step += 1

    def check_game_over(self):
        """
        Метод для проверки завершения игры и определения победителя.
        """
        if self.stop:
            return True
        else:
            return False

    def save_game_state(self):
        """
        Сохраняем список победителей в JSON
        """
        # Удаляем последнего победителя
        del self.winners_list[4]
        # Добавляем нового победителя в начало списка
        self.winners_list.insert(0, self.winner)
        # Сохраняем список победителей в JSON
        self.write_json(self.winners_list, "winners.json")


class GameManager:
    """
    Класс GameManager : Этот класс принимает экземпляры классов JsonFile , Cities и CityGame
    """

    def __init__(self, json_file, city_game_, cities_set):
        """
        Инициализация
        :param json_file: имя JSON-файла
        """
        self.json_file = json_file
        self.cities_set = cities_set
        self.city_game = city_game_

    def __call__(self):
        self.run_game()

    def run_game(self):
        """
        Метод для запуска игры
        """
        # Выводим список победителей
        self.city_game.print_winners()
        # Запускаем игру
        self.city_game.start_game()
        # Цикл игры пока не завершена
        while not self.city_game.check_game_over():
            # Ход компьютера
            if not self.city_game.check_game_over():
                self.city_game.computer_turn()
                if self.city_game.check_game_over():
                    break
            else:
                break
            # Ход человека
            while True:
                # Запрашиваем ввод города
                city_input = input("Введите название города: ")
                # Проверяем завершение игры
                if not self.city_game.check_game_over():
                    # Если пользователь ввел "стоп" - завершаем игру
                    if self.city_game.stop_game(city_input):
                        break
                    # Проверяем корректность ввода по последнему символу в названии города
                    if not self.city_game.last_char_check(city_input):
                        continue
                    # Проверяем вхождение в список "плохих" букв
                    if self.city_game.included_in_badchar(city_input):
                        continue
                    # Ходим
                    self.city_game.human_turn(city_input)
                    # Проверяем завершение игры и если да - выходим из цикла
                    if self.city_game.check_game_over():
                        break
                    break
                else:
                    break
        # Выводим список победителей
        self.city_game.print_winners()


cities = Cities()
cities_set = cities.get_cities()
city_game = CityGame(cities_set)
game_manager = GameManager(JsonFile(), city_game, cities_set)

if __name__ == '__main__':
    game_manager()
