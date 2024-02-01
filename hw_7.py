import os

os.system('cls')

new_list = set()
data_lst = ['1', '2', '3', '4d', 5]
for item in data_lst:
    try:
        new_list.add(int(item))
    except ValueError:
        print(f'Данные невалидны {item}')
        continue

print(f'Итоговый список {new_list}')

nums_new = set()
# фиксированный проверочный список:
# nums_list = ['+77053й183958','+87773183958','877731!83958','+(777)731+3958','+7(777)-731-83-58','+7(777) 731 83 58',
#  '+97(777) 731 83 58','+97(777) 731 83 в58','+07(77) 731 83 58']
# проверочный список:
# 77053183958;+77053й183958;+87773183958;877731!83958;+(777)731+3958;+7(777)-731-83-58;+7(777) 731 83 58;+97(777) 731 83 58;+97(777) 731 83 в58;+07(77) 731 83 58
nums_list = input("Введит номера телефонов через точку с запятой (без пробелов): ").split(';')
for num in nums_list:
    num_old = num  # сохраняем старый номер телефона
    num = num.replace("-", "")  # удаляем все знаки "-"
    num = num.replace(" ", "")  # удаляем все пробелы
    num = num.replace("(", "")  # удаляем все скобки
    num = num.replace(")", "")  # удаляем все скобки
    if num[0] == "+":  # удаляем первый символ, если вдруг присутствует "+"
        num = num[1:]
    try:
        if not num.isdigit():
            raise ValueError(f'Неправильный формат номера телефона {num_old}. Номер должен состоять из цифр')
        if len(num) != 11:
            raise ValueError(f'Неправильный формат номера телефона {num_old}. Номер должен состоять из 11 цифр')
        if num_old[:2] != '+7' and num_old[0] != '8':
            raise ValueError(f'Неправильный формат номера телефона {num_old}. Номер должен начинаться с +7 или 8')
        else:
            nums_new.add(num_old)
    except ValueError as error:
        print(error)
        continue
print(f'Итоговый список правильных телефонов {nums_new}')
