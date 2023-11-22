#конветер секунд
total_seconds = int(input("Введите количество секунд: "))
hours = int(total_seconds/3600) #получаем часы
minutes = int((total_seconds-hours*3600)/60) #получаем минуты
seconds = int(total_seconds-hours*3600-minutes*60) #получаем секунды
print(f'В указанном количестве секунд {total_seconds} \nЧасов: {hours} \nМинут: {minutes} \nСекунд: {seconds}')


#конвертер градусов цельсия
celsius = int(input("Введите количество градусов цельсия: "))
kelvin = celsius + 273.15
fahrenheit = celsius * 1.8 + 32
rheomur = celsius * 0.8
print(f'В указанном количестве градусов цельсия {celsius} \nГрадусов Кельвина: {kelvin:.2f} \nГрадусов Фаренгейта: {fahrenheit:.2f}'
      f' \nГрадусов Реомюра: {rheomur:.2f}')
