from flask import Flask, request
from resources import EntryManager, Entry

app = Flask(__name__)

FOLDER = '/tmp/'

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/api/entries/")
def get_entries():
    entry_manager = EntryManager(FOLDER) # Инициализируйте объект класса EntryManager, указав FOLDER в качестве data_path
    entry_manager.load() # загрузит все записи из исходной папки FOLDER в память компьютера (в аттрибут объекта entry_manager.entries)
    result = [] # вернуть лист
    for entry in entry_manager.entries:
        result.append(entry.json()) # в лист добавить entry.json() для каждой записи
    return result

@app.route('/api/save_entries/', methods=['POST'])
def save_entries():
    entry_manager = EntryManager(FOLDER) # Инициализируйте менеджер
    data = request.get_json() # Заполучите JSON из запроса
    for entry_data in data: # При помощи цикла for пройдитесь по элементам листа записей
        entry = Entry.from_json(entry_data) # При помощи метода Entry.from_json - инициализируйте запись
        entry_manager.entries.append(entry) # Добавьте запись в лист entry_manager.entries
    entry_manager.save() # сохранит все имеющиеся записи
    return {'status': 'success'} # Функция должна возвращать какой-нибудь непустой ответ

# Это необходимо для того, чтобы front-end, находящийся на одном домене (удаленном сайте), мог общаться с back-end'ом, находящимся на другом домене (вашем локальном компьютере) через браузер
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)