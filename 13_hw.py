from pprint import pprint

from marvel import full_dict


# Задание 2 (1 2 55 6 11 aa 7 gg)
def to_int(num_str: str) -> int | None:
    """
    Преобразуем строку в число, если введено не число меняет на None
    :param num_str: строка
    :return: либо число, либо None
    """
    if num_str.isdigit():
        num = int(num_str)
    else:
        num = None
    return num


# Пользовательский ввод чисел
num_input = input('Введите числа через пробел: ').split(' ')
# Преобразуем в список числа с помощью map
num_to_int = list(map(to_int, num_input))
# Выводим список
print('Задание №2:')
print(num_to_int)
print('')


# Задание 3
def filtered_marvel_dict(items: tuple) -> bool:
    """
    Проверка на вхождение введенных чисел пользователм в словарь
    :param items: Входной кортеж для анализа
    :return: Возвращает True или False
    """
    # распаковываем кортеж
    key = items[0]
    if key in num_to_int:
        return True
    return False


# Фильтруем словарь
filtered_dict: dict = dict((filter(filtered_marvel_dict, full_dict.items())))
# Выводим словарь
print('Задание №3:')
pprint(filtered_dict)
print('')

# Задание 4
# Формируем новое множество режиссеров (по ключу director)
director_set: set = set(director['director'] for director in full_dict.values())
# Выводим множество
print('Задание №4:')
pprint(director_set)
print('')

# Задание 5
# Формируем новый словарь и преобразуем ключ year в строку
new_marvel_dict: dict = {k: {key: str(value) if key == 'year' else value for key, value in v.items()} for k, v in
                         full_dict.items()}
# Выводим словарь
print('Задание №5:')
pprint(new_marvel_dict)
print('')


# Задание 6
def filtered_marvel_dict2(items: tuple) -> bool:
    """
    Функция для фильтрации словаря
    :param items: входной словарь для анализа первой буквы
    :return:  возвращает True или False
    """

    value = items[1]
    if value['title'][0].upper() == 'Ч':
        return True
    return False


# Фильтруем словарь
filtered_dict2 = dict(filter(filtered_marvel_dict2, full_dict.items()))
# Выводим словарь
print('Задание №6:')
pprint(filtered_dict2)
print('')

# Задание 7
# Сортируем словарь по названию (title)
sorted_marvel: dict = dict(sorted(full_dict.items(), key=lambda value: value[1]['title']))
# Выводим словарь
print('Задание №7:')
pprint(sorted_marvel, sort_dicts=False)
print('')

# Задание 8
# Сортируем словарь по продюсеру и названию (producer, title)
sorted_marvel_2params: dict = dict(
    sorted(full_dict.items(), key=lambda value: (value[1]['producer'], value[1]['title'])))
# Выводим словарь
print('Задание №8:')
pprint(sorted_marvel_2params, sort_dicts=False)
print('')

# Задание 9
# Фильтруем словарь по id(введенному пользователем в задании 2) и сортируем по режиссеру ('director').
sorted_marvel2: dict = dict(
    sorted(filter(filtered_marvel_dict, full_dict.items()), key=lambda value: value[1]['director']))
# Выводим словарь
print('Задание №9:')
pprint(sorted_marvel2, sort_dicts=False)
print('')

# Задание 10
# На сколько я понял эти ошибки из-за неглубокого анализа mypy словаря-словарей
# (хотя может и я накосячил с кодом, но вроде отрабатывает все верно)
# lesson_13_hw.py:49: error: Value of type "object" is not indexable  [index]
# lesson_13_hw.py:55: error: "object" has no attribute "items"  [attr-defined]
# lesson_13_hw.py:83: error: Value of type "object" is not indexable  [index]
# lesson_13_hw.py:91: error: Value of type "object" is not indexable  [index]
# lesson_13_hw.py:99: error: Value of type "object" is not indexable  [index]
# Found 5 errors in 1 file (checked 1 source file)
