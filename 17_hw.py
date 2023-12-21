import os
from abc import ABC, abstractmethod

os.system("cls")


# Абстрактный класс устройства
class SmartDevice(ABC):
    # Имя устройства
    device_name: str = ''

    def __init__(self):
        self.state = False
        self.device_name = SmartDevice.device_name

    # Абстрактный метод управления (включить/выключить)
    @abstractmethod
    def on_off(self):
        pass

    # Абстрактный метод получения состояния
    @abstractmethod
    def get_state(self):
        pass


# Класс умная лампа
class SmartLamp(SmartDevice):
    def __init__(self):
        super().__init__()
        # Начальная яркость 0
        self.brightness = 0

    # Получение состояния
    def get_state(self):
        print(f'Устройство {self.device_name} состояние: активность - {self.state}; яркость - {self.brightness}')

    # Включение/выключение
    def on_off(self):
        self.state = not self.state

    # Изменение яркости
    def adjust_brightness(self, brightness: int):
        self.brightness = brightness
        print(f'Устройство {self.device_name} установлена яркость: {brightness}')


# Класс умный датчик дыма
class SmartSmokeSensor(SmartDevice):
    def __init__(self):
        super().__init__()
        # Начальное состояние дыма False
        self.flag: bool = False

    # Получение состояния
    def get_state(self):
        print(f'Устройство {self.device_name} состояние: активность - {self.state}')

    # Включение/выключение
    def on_off(self):
        self.state = not self.state

    # Проверка дыма
    def check_smoke(self):
        return self.flag


# Класс умный датчик влажности
class SmartHumidifier(SmartDevice):
    def __init__(self):
        super().__init__()

    # Получение состояния
    def get_state(self):
        print(f'Устройство {self.device_name} состояние: активность - {self.state}; влажность - {self.humidity}')

    # Включение/выключение
    def on_off(self):
        self.state = not self.state

    # Изменение влажности
    def set_humidity(self, humidity: int):
        self.humidity = humidity
        print(f'Устройство {self.device_name} установлена влажность: {humidity}')


# Миксин срочного сообщения
class AlarmMixin:

    def send_alarm(self, msg: str):
        print(msg)


# Миксин подключения к WiFi
class ConnectingToWiFiMixin:

    def __init__(self):
        self.device_name = None

    # Подключение к WiFi
    def connect_to_wifi(self, ssid: str, password: str):
        print(f"Устройство {self.device_name} - подключаемся к WiFi - Логин:{ssid} Пароль:{password}")


# Миксин рабочего расписания
class WorkScheduleMixin:
    schedule: dict = {}

    def __init__(self):
        self.device_name = None

    # Установка рабочего расписания
    def set_schedule(self, schedule: dict):
        self.schedule = schedule
        print(f"Устройство {self.device_name} - устанавливаем рабочее расписание: {schedule}")

    # Получение рабочего расписания
    def get_schedule(self):
        print(f"Устройство {self.device_name} - получаем рабочее расписание: {self.schedule}")


# Класс умная лампа в спальне
class SmartLampInBedroom(SmartLamp, ConnectingToWiFiMixin):
    def __init__(self):
        super().__init__()


# Класс умный датчик дыма на кухне
class SmartSmokeSensorInKitchen(SmartSmokeSensor, AlarmMixin, ConnectingToWiFiMixin):
    def __init__(self):
        super().__init__()


# Класс умный увлажнитель в спальне
class SmartHumidifierInLivingRoom(SmartHumidifier, WorkScheduleMixin, ConnectingToWiFiMixin):
    def __init__(self):
        super().__init__()


# Создание экземпляра умной лампы
LampInBedroom = SmartLampInBedroom()
# Задаем имя устройства
LampInBedroom.device_name = 'Лампа в спальне'
# Подключаемся к WiFi
LampInBedroom.connect_to_wifi('Homelan', 'Password!123')
# Получаем состояние
LampInBedroom.get_state()
# Установляем яркость 50%
LampInBedroom.adjust_brightness(50)
# Включаем/выключаем
LampInBedroom.on_off()
# Получаем состояние
LampInBedroom.get_state()
# Установляем яркость 100%
LampInBedroom.adjust_brightness(100)
# Получаем состояние
LampInBedroom.get_state()

# Создание экземпляра умного датчика дыма
SmokeSensorInKitchen = SmartSmokeSensorInKitchen()
# Задаем имя устройства
SmokeSensorInKitchen.device_name = 'Датчик дыма на кухне'
# Подключаемся к WiFi
SmokeSensorInKitchen.connect_to_wifi('Homelan', 'Password!123')
# Получаем состояние
SmokeSensorInKitchen.get_state()
# Установка флага наличие дыма на кухне
SmokeSensorInKitchen.flag = False
# Проверка дыма
if SmokeSensorInKitchen.check_smoke():
    SmokeSensorInKitchen.send_alarm('Обнаружен дым на кухне!')


# Создание экземпляра умного увлажнителя
HumidifierInLivingRoom = SmartHumidifierInLivingRoom()
# Задаем имя устройства
HumidifierInLivingRoom.device_name = 'Увлажнитель в спальне'
# Подключаемся к WiFi
HumidifierInLivingRoom.connect_to_wifi('Homelan', 'Password!123')
# Устанавливаем рабочее расписание
HumidifierInLivingRoom.set_schedule({'ON': '08:00', 'OFF': '22:00'})
# Включаем/выключаем
HumidifierInLivingRoom.on_off()
# Задаем влажность 75%
HumidifierInLivingRoom.set_humidity(75)
# Получаем состояние
HumidifierInLivingRoom.get_state()
# Устанавливаем влажность 0%
HumidifierInLivingRoom.set_humidity(0)
# Получаем состояние
HumidifierInLivingRoom.get_state()
# Получаем расписание
HumidifierInLivingRoom.get_schedule()
