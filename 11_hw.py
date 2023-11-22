import json
from prettytable import PrettyTable
# import os  # очищаю экран os.system('cls') от лишней информации в консоле
# os.system('cls')

# from cities import cities_list
cities_list_use = []

# очищаем список городов от "плохих букв" и записываем в JSON
# cities_list_set = set({city['name'] for city in cities_list})
# cities_list_set_clear = set()
# cities_list_set_badchar = set()
# for last_char in cities_list_set:
#     for first_char in cities_list_set:
#         if last_char[-1].lower() == first_char[0].lower(): 
#             cities_list_set_clear.add(last_char)
#             break
# cities_list_set_badchar= cities_list_set.difference(cities_list_set_clear)
# with open("cities.json", "w", encoding="utf-8") as file:
# json.dump(list(cities_list_set_clear), file, ensure_ascii=False, indent=4)
# with open("cities_bad.json", "w", encoding="utf-8") as file:
# json.dump(list(cities_list_set_badchar), file, ensure_ascii=False, indent=4)

# загружаем список городов+список городо с 'плохими буквами'
with open("cities.json", "r", encoding="utf-8") as file:
    cities_list_set_clear = set(json.load(file))
with open("cities_bad.json", "r", encoding="utf-8") as file:
    cities_list_set_badchar = set(json.load(file))

# выводим список победителей c проверкой на существование файла победителей
try:
    with open("winners.json", "r", encoding="utf-8") as file:
        winners_list = json.load(file)
except:
    winners_list = ['0', '0', '0', '0', '0']

winners_table = PrettyTable()
winners_table.field_names = ["№ п/п", "Победитель"]
for index in range(len(winners_list)):
    winners_table.add_row([index + 1, winners_list[index]])
print('Таблица победителей:')
print(winners_table)


# print()
stop = False
last_char = ''
step= 1

while not stop:
    # старт программы последний символ пустой
    if last_char == '':
        city_name = input("Введите название города или стоп чтобы остановить игру : ")
        if city_name.title() in cities_list_set_badchar:  # проверяем на вхождение в список "плохих букв"
            print(f'Город {city_name.title()} в списке \'плохих букв\'. Попробуйте еще раз.')
            continue
    else:
        while True:  # ждем ввод города
            city_name = input(f"Введите название города на букуву {last_char.upper()} или стоп чтобы остановить игру: ")
            if city_name.lower() == "стоп":
                stop = True
                break
            if city_name.title() in cities_list_set_badchar:  # проверяем ввод города на вхождение в список "плохих букв"
                print(f'Город {city_name.title()} в списке \'плохих букв\'. Попробуйте еще раз.')
                continue
            if city_name[0].lower() == last_char.lower():
                break
            else:
                print("Некорректный ввод. Попробуйте еще раз.")
    if (city_name.lower() != "стоп"):
        if (city_name.title() in cities_list_set_clear):  # вхождение в список городо
            cities_list_set_clear.discard(city_name.title())  # удаляем из списка, что бы не повторялся город
            cities_list_use.append(city_name.title())  # добавляем в новый список для дальнейшей проверке на вхождение
            last_char = city_name[-1]
            print(f'Вы назвали город {city_name.title()}. Компьютеру город на {last_char.upper()}')
            step += 1
            for city_comp in cities_list_set_clear:  # компьютер выбирает город
                if city_comp[0].lower() == last_char.lower():
                    last_char = city_comp[-1]
                    print(f'Компьютер называет город {city_comp.title()}. Вам город на {last_char.upper()}')
                    cities_list_set_clear.discard(city_comp.title())  # удаляем из списка, что бы не повторялся город
                    cities_list_use.append(
                        city_comp.title())  # добавляем в новый список для дальнейшей проверке на вхождение
                    step += 1
                    break
            else:
                stop = True
                print(f'Компьютер не может назвать город. Вы выиграли на {step} ходу!')
                # обнуляем список победителей
                del winners_list[4]
                winners_list.insert(0, 'Пользователь')
                with open("winners.json", "w", encoding="utf-8") as file:
                    json.dump(winners_list, file, ensure_ascii=False, indent=4)

                break
        else:
            if (city_name.title() in cities_list_use):
                print(f'Город {city_name.title()} уже называли. Вы проиграли на {step} ходу!')
                # обнуляем список победителей
                del winners_list[4]
                winners_list.insert(0, 'Компьютер')
                with open("winners.json", "w", encoding="utf-8") as file:
                    json.dump(winners_list, file, ensure_ascii=False, indent=4)

                stop = True
            else:
                print(f'Город {city_name.title()} не существует. Вы проиграли на {step} ходу!')
                # обнуляем список победителей
                del winners_list[4]
                winners_list.insert(0, 'Компьютер')
                with open("winners.json", "w", encoding="utf-8") as file:
                    json.dump(winners_list, file, ensure_ascii=False, indent=4)

                stop = True
    else:
        stop = True
        print(f'Вы остановили игру. Вы проиграли! на {step} ходу')
        # обнуляем список победителей
        del winners_list[4]
        winners_list.insert(0, 'Компьютер')
        with open("winners.json", "w", encoding="utf-8") as file:
            json.dump(winners_list, file, ensure_ascii=False, indent=4)
