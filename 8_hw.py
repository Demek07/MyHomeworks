import os
from marvel import full_dict
from pprint import pprint
os.system('cls')
stage = {
    1:"Первая фаза",
    2:"Вторая фаза",
    3:"Третья фаза",
    4:"Четвертая фаза",
    5:"Пятая фаза",
    6:"Шестая фаза",
}

while True: #ждем правильный ввод
    try:
        phase = input("Введите цифрами одну фазу: ")
        if not phase.isdigit(): # проверяем что введена цифра
            raise TypeError("Введена не цифра.")
        else:
            phase = int(phase) 
            if phase not in stage: # проверяем существование фазы
                raise ValueError(f"Введеная фаза - {phase} не существует.")
        break 
    except (TypeError, ValueError) as error:
        print(error)

search_phase = stage.get(phase)
for items in full_dict: # перебираем все ключи
    if full_dict[items].get('stage') == search_phase:   # если совпадение найдено, то печатаем
        pprint(full_dict[items])


