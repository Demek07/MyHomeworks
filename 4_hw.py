input_phone = input("Введите номер телефона: ")
phone = input_phone.replace("-", "")
phone = phone.replace(" ", "")
phone = phone.replace("(", "")
phone = phone.replace(")", "")
phone = phone.replace("+", "")
is_digit = False
is_start = False
is_len_number = False
message = ''

if phone.isdigit():
    is_digit=True
else:
    message += "Телефон должен содержать только цифры\n"
if phone[0] == "7" or phone[0] == "8":
    is_start = True
else:
    message += "Телефон должен начинаться с 7 или 8\n"
if len(phone) == 11:
    is_len_number = True
else:
    message += "Телефон должен содержать 11 цифр\n"
if is_len_number and is_digit and is_start:
    message += f"Введеный телефон: {input_phone} - корректный"
else:
    message += f"Введеный телефон: {input_phone} - не корректный"

print(message)


input_password = input("Введите пароль: ")
is_special_character = False
is_space = False
is_registr = False
is_len_password = False
res_message = ''
input_pass = input_password
input_pass = input_pass.replace(" ", "") #удаляем пробелы так как они попадают в спецсимволы

if not (input_pass.isalnum() or input_pass.isalpha()):
    is_special_character = True
else:
    res_message += f"Пароль должен содержать хотя бы один спецсимвол\n"
if len(input_password) >= 7:
    is_len_password = True
else:
    res_message += f"Длина пароля должна быть не менее 7 символов\n"
if input_password.find(" ") == -1:
    is_space = True
else:
    res_message += f"Пароль не должен содержать пробелы\n"
if not (input_password.isupper() or input_password.islower()):
    is_registr = True
else:
    res_message += f"Пароль должен содержать символы разных регистров\n"
if is_special_character and is_len_password and is_space and is_registr:
    res_message += f"Введенный пароль: {input_password} - корректный"
else:
    res_message += f"Введенный пароль: {input_password} - не корректный"
print(res_message)