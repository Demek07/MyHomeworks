import ast
import csv
import json

# Список списков для тестирования
list_1 = [['Name', 'Ivan'], ['Age', '25'], ['City', 'Moscow'], ['Country', 'Russia']]
# Имена файлов
file_name_csv = "lesson_16_hw.csv"
file_name_json = "lesson_16_hw.json"
file_name_txt = "lesson_16_hw.txt"


def list_to_dict(list_in: list) -> list:
    """
    Преобразование списка в словарь
    :param list_in: Входящий список
    :return: возвращаем список словарей
    """
    list_of_dicts: list = [{item[0]: item[1]} for item in list_in]
    return list_of_dicts


def dict_to_list(dict_in: list) -> list:
    """
    Преобразование словаря в список
    :param dict_in: Входящий словарь
    :return: возвращаем список словарей
    """
    dict_of_lists = []
    for item in dict_in:
        for key, value in item.items():
            dict_of_lists.append([key, value])
    return dict_of_lists


class CsvFileHandler:
    def __init__(self, filepath):
        self.filepath = filepath

    def writer_to_csv(self, file, data, as_dict=False):
        """
        Запись в файл
        :param file: Имя файла
        :param data: Данные
        :param as_dict: Флаг записи в словарь
        """
        # Проверка флага словаря
        if as_dict:
            # Проверяем, что это список словарей
            if isinstance(data[0], dict):
                # Записываем данные в файл
                writer = csv.writer(file)
                writer.writerow(data)
            else:
                # Если это не список словарей, то преобразуем его в список словарей и записываем
                writer = csv.writer(file)
                writer.writerow(list_to_dict(data))
        else:
            # Если флага словаря нет - просто записываем данные
            writer = csv.writer(file)
            writer.writerow([",".join(sublist) for sublist in data])

    def read_file(self, as_dict=False):
        """
        Чтение из файла
        :param as_dict: Флаг словаря (в каком виде читаем из файла)
        """
        # Пытаемся открыть файл на чтение
        try:
            # Открываем файл
            with open(self.filepath, "r", encoding="windows-1251") as file:
                reader = csv.reader(file)
                # Проверяем флаг словаря
                if as_dict:
                    # Читаем данные
                    for row in reader:
                        # Если находим ":" - признак словаря, то преобразуем в словарь и печатаем
                        if ':' in row[0]:
                            reader_list = [ast.literal_eval(text) for text in row]
                            print(reader_list)
                        else:
                            # Если не находим ":" - признак словаря, то преобразуем в словарь и печатаем
                            reader_list = [sublist.split(',') for sublist in row]
                            print(list_to_dict(reader_list))
                else:
                    # Если флаг словаря нет - просто читаем
                    for row in reader:
                        # Если нашли ":" - признак словаря, то преобразуем в список и печатаем
                        if ':' in row[0]:
                            reader_list = []
                            for text in row:
                                txt = ast.literal_eval(text)
                                reader_list.append(txt)
                            print(dict_to_list(reader_list))
                        else:
                            # Если не нашли ":" - признак словаря, то печатаем
                            reader_list = [sublist.split(',') for sublist in row]
                            print(reader_list)
        # Если не удалось открыть файл - печатаем ошибку и возвращаем тестовый список
        except FileNotFoundError:
            return list_1

    def write_file(self, data, as_dict=False):
        """
        Запись в файл
        :param data: Данные
        :param as_dict: Флаг словаря
        """
        with (open(self.filepath, 'w', encoding='windows-1251', newline='') as file):
            self.writer_to_csv(file, data, as_dict)

    def append_file(self, data, as_dict=False):
        """
        Дозапись в файл
        :param data: Данные
        :param as_dict: Флаг словаря
        """
        with open(self.filepath, 'a', encoding='windows-1251', newline='') as file:
            self.writer_to_csv(file, data, as_dict)


class JsonFileHandler:
    def __init__(self, filepath):
        self.filepath = filepath

    def read_file(self, as_dict=False):
        """
        Чтение из файла JSON
        :param as_dict: Флаг словаря
        """
        # Пытаемся открыть файл на чтение
        with open(self.filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
        # Проверяем флаг словаря
        if as_dict:
            # Если прочитанные данные - словарь, то печатаем
            if isinstance(data[0], dict):
                print(data)
            else:
                # Если прочитанные данные - не словарь, то преобразуем в словарь и печатаем
                print(list_to_dict(data))
        # Если флаг словаря нет и полученные данные словарь - преобразуем в список и печатаем
        elif isinstance(data[0], dict):
            print(dict_to_list(data))
        # Если флаг словаря нет и полученные данные не словарь - просто печатаем
        else:
            print(data)

    def write_file(self, data, as_dict=False):
        """
        Запись в файл JSON
        :param data: Данные
        :param as_dict: Флаг словаря
        """
        # Проверяем флаг словаря
        if as_dict and not isinstance(data[0], dict):
            data = list_to_dict(data)
        with open(self.filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    @staticmethod
    def append_file(self, data, as_dict=False):
        """
        Дозапись в файл JSON
        Райзим ошибку, так как данный тип файла не поддерживает операцию дописывания
        """
        raise Exception('Данный тип файла не поддерживает операцию дописывания')


class TxtFileHandler:
    def __init__(self, filepath):
        self.filepath = filepath

    def read_file(self, as_dict=False):
        """
        Чтение из файла TXT
        :param as_dict: Флаг словаря
        """
        # Пытаемся открыть файл
        with open(self.filepath, "r") as file:
            # Читаем
            data = file.read()
            # Печатаем
            print(data)

    def write_file(self, data, as_dict=False):
        """
        Запись в файл TXT
        :param data: Данные
        :param as_dict: Флаг словаря
        """
        # Пытаемся открыть файл
        with open(self.filepath, "w") as file:
            # Записываем
            file.write(' '.join(map(str, data)))

    def append_file(self, data, as_dict=False):
        """
        Дозапись в файл TXT
        :param data: Данные
        :param as_dict: Флаг словаря
        """
        # Пытаемся открыть файл
        with open(self.filepath, "a") as file:
            # Записываем
            file.write(' '.join(map(str, data)))


# Создаем экземпляры классов CsvFileHandler
# Дозапись в файл
file_append_csv = CsvFileHandler(file_name_csv)
# Запись в файл
file_write_csv = CsvFileHandler(file_name_csv)
# Чтение из файла
file_read_csv = CsvFileHandler(file_name_csv)
# Создаем экземпляры классов JsonFileHandler
# Дозапись в файл
file_append_json = JsonFileHandler(file_name_json)
# Запись в файл
file_write_json = JsonFileHandler(file_name_json)
# Чтение из файла
file_read_json = JsonFileHandler(file_name_json)
# Создаем экземпляры классов TxtFileHandler
# Дозапись в файл
file_append_txt = TxtFileHandler(file_name_txt)
# Запись в файл
file_write_txt = TxtFileHandler(file_name_txt)
# Чтение из файла
file_read_txt = TxtFileHandler(file_name_txt)

files = [file_append_csv, file_write_csv, file_read_csv, file_append_json, file_write_json, file_read_json,
         file_append_txt, file_write_txt, file_read_txt]

for file in files:
    # Запись в файл, признак словаря
    file.write_file(list_1, True)
    # Запись в файл, без признака словаря
    file.write_file(list_1, False)
    # Дозапись в файл, признак словаря
    file.append_file(list_1, True)
    # Дозапись в файл, без признака словаря
    file.append_file(list_1, False)
    # Чтение из файла, признак словаря
    file.read_file(True)
    # Чтение из файла, без признака словаря
    file.read_file()
