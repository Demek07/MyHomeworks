import csv
from typing import Callable


# проверка корректности пароля
def password_validator(length: int = 8, uppercase: int = 1, lowercase: int = 1, special_chars: int = 1) -> Callable:
    """
    Проверка пароля
    :param length: минимальная длина
    :param uppercase: количество букв верхнего регистра
    :param lowercase: количество букв нижнего регистра
    :param special_chars: количество спецсимволов
    """

    def decorator(func: Callable) -> Callable:
        def wrapper(username_, password_):
            # Обнуляем итоговое сообщение об ошибке
            res_message = ''
            password = password_
            # Удаляем пробелы так как они попадают в спецсимволы
            input_pass = password.replace(" ", "")
            # Длина пароля
            length_sum = len(password)
            # Считаем количество букв верхнего регистра
            uppercase_sum = sum(i.isupper() for i in password)
            # Считаем количество букв нижнего регистра
            lowercase_sum = sum(i.islower() for i in password)
            # Считаем количество спец-знаков
            special_chars_sum = len(input_pass) - (sum(i.isalnum() for i in input_pass))
            # Блок проверок
            if length_sum < length:
                res_message += f'Длина пароля должна быть не менее {length} символов\n'
            if uppercase_sum < uppercase:
                res_message += f'Количество букв верхнего регистра должно быть не менее {uppercase} символов\n'
            if lowercase_sum < lowercase:
                res_message += f'Количество букв нижнего регистра должно быть не менее {lowercase} символов\n'
            if special_chars_sum < special_chars:
                res_message += f'Количество спец-знаков должно быть не менее {special_chars} символов\n'
            # Если есть ошибки - выдаем исключение
            if res_message != '':
                raise ValueError(res_message)
            return func(username_, password_)

        return wrapper

    return decorator


def username_validator() -> Callable:
    """
    Проверка имени пользователя на наличие пробелов и пустого имени
    """

    def decorator(func: Callable) -> Callable:
        def wrapper(username__, password__):
            res_message = ''
            # Проверка на наличие пробелов
            if username__.find(" ") != -1:
                res_message += f"Имя пользователя не должно содержать пробелы\n"
            # Проверка на пустое имя
            if len(username__) == 0:
                res_message += f"Имя пользователя не должно быть пустым\n"
            # Если есть ошибки - выдаем исключение
            if res_message != '':
                raise ValueError(res_message)
            return func(username__, password__)

        return wrapper

    return decorator


# декорируем функцию с заданными параметрами
@password_validator(length=10, uppercase=2, lowercase=2, special_chars=2)
@username_validator()
def register_user(username: str, password: str) -> None:
    """
    Регистрация пользователя
    :param username: Имя пользователя
    :param password: Пароль
    """
    # Если проверка прошла успешно - записываем данные в файл
    with open('users.csv', 'a', encoding='windows-1251', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow([username, password])


try:
    # Отправляем на проверку данные
    register_user("JohnDoe", "PЗasswor123!!!")
except ValueError as e:
    # Выводим ошибку
    print(e)
else:
    # Если ошибки нет выводим сообщение
    print("Регистрация прошла успешно!")

# Проверка mypy.
# PS C:\...> mypy lesson_14_hw_.py
# Success: no issues found in 1 source file
