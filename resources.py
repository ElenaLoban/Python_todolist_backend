import os
from typing import List  # указывает на тип list



def print_with_indent(value, indent=0):
    indentation = '\t' * indent
    print(f'{indentation}{value}')


class Entry:
    def __init__(self, title, entries=None, parent=None):
        self.title = title
        if entries is None:
            entries = []
        self.entries = entries
        self.parent = parent

    def add_entry(self, entry):
        self.entries.append(entry)
        entry.parent = self

    def print_recursively(self):
        for entry in self.entries:
            print(entry)
            if isinstance(entry, Entry):
                entry.print_recursively()

    def print_entries(self, indent=0):
        print_with_indent(self, indent)
        for entry in self.entries:
            entry.print_entries(indent=indent + 1)

    def json(self):
        res = {
            "title": self.title,
            "entries": []
        }  # создала структуру dict
        for entry in self.entries:
            res["entries"].append(entry.json())  # заменяю строку на словарь
        return res  # возвращаю словарь

    @classmethod
    def from_json(cls, value):
        entry = cls(value['title'])  # принимаем словарь
        for sub_entry in value.get('entries', []):  # для получения вложенных записей
            entry.add_entry(cls.from_json(sub_entry))  # использование метода from_json
        return entry  # возвращаем запись

    def __str__(self):
        return self.title

    def save(self, path):
        self.path = os.listdir(path)  # присвоили значение переменной
        content = self.json()  # вернули словарь
        with open(f'/tmp/{self.title}.json', 'w') as f:  # сохранили в формате json
            json.dump(content, f)

    @classmethod
    def load(cls, filename):
        with open(filename, 'r') as file:  # Открыли filename в режиме чтения
            data = json.load(file)  # Загружать контент файла в dict
            obj = cls.from_json(data)  # создаю объект из словаря
            return obj





class EntryManager:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.entries: List[Entry] = []

    def save(self):
        for entry in self.entries:
            entry.save(self.data_path)  # метод save определен в каждой из записей

    def load(self):
        if not os.path.isdir(self.data_path):  # если пути/каталога не существует
            os.makedirs(self.data_path)  # рекурсивно создает все промежуточные каталоги, если они не существуют.
        else:
            for filename in os.listdir(self.data_path):
                if filename.endswith('json'):  # проверка, что файл заканчивается на .json
                    entry = Entry.load(os.path.join(self.data_path, filename))  # загрузка записи из файла
                    self.entries.append(entry)  # добавляем загруженный entry в self.entries
        return self

    def add_entry(self, title):
        self.entries.append(Entry(title))