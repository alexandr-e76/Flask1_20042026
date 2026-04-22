from flask import Flask, jsonify, request, g, abort
from typing import Any
from random import choice
from http import HTTPStatus
from pathlib import Path
import sqlite3
from werkzeug.exceptions import HTTPException

BASE_DIR = Path(__file__).parent
path_to_db = BASE_DIR / "store.db" # <- тут путь к БД
# Используем так:
connection = sqlite3.connect(path_to_db)

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(path_to_db)
    return db

@app.teardown_appcontext
def close_connection(exception):   
    db = getattr(g, '_database', None)
    if db is None:
        db.close()

@app.errorhandler(HTTPException)    # Функция для перевата HTTP ошибок и возврата в виде JSON
def handle_exception(e):
    return jsonify({"message": e.description}), e.code

create_table = """
CREATE TABLE IF NOT EXISTS quotes (
id INTEGER PRIMARY KEY AUTOINCREMENT,
author TEXT NOT NULL,
text TEXT NOT NULL,
rating INTEGER NOT NULL
);
"""
connection = sqlite3.connect("name.db")
cursor = connection.cursor()
cursor.execute(create_table)
connection.commit()
cursor.close()
connection.close()

# about_me = {
#     "name": "Александр",
#     "surname": "Егоров",
#     'email': "egorov1011@gmail.com"
# }
# # quotes = [
# {
# "id": 3,
# "author": "Rick Cook",
# "text": """Программирование сегодня — это гонка разработчиков программ, стремящихся писать программы с
# большей и лучшей идиотоустойчивостью, и вселенной, которая
# пытается создать больше отборных идиотов. Пока вселенная
# побеждает."""
# },
# {
# "id": 5,
# "author": "Waldi Ravens",
# "text": "Программирование на С похоже на быстрые танцы \
# на только что отполированном полу людей с острыми бритвами в \
# руках."
# },
# {
# "id": 6,
# "author": "Mosher’s Law of Software Engineering",
# "text": "Не волнуйтесь, если что-то не работает. Если \
# бы всё работало, вас бы уволили."
# },
# {
# "id": 8,
# "author": "Yoggi Berra",
# "text": "В теории, теория и практика неразделимы. На \
# практике это не так."
# },
# ]
# Нужно больше цитат? https://tproger.ru/devnull/programming-quotes/По url: /quotes , вернем полный список цитат
# @app.route("/")
# def hello_world():
#     return "Hello, World!"

@app.route("/about")
def about():
    return about_me

@app.route("/quotes")
def get_quotes()->list[dict[str, any]]:
    select_quotes = "SELECT * from quotes"

# Подключение в БД
    connection = sqlite3.connect("store.db")
# Создаем cursor, он позволяет делать SQL-запросы
    cursor = get_db.cursor()
# Выполняем запрос:
    cursor.execute(select_quotes)
# Извлекаем результаты запроса
    # quotes_db = cursor.fetchall() # Здесь получаем список кортежей
    # print(f"{quotes_db =}")
# # Закрыть курсор:
#     cursor.close()
# # Закрыть соединение:
#     connection.close()
# #Поготовка данных для отправки в праильном формате
#Необходимо выполнить преобразование:
#list[tuple] -> list[dict]
    keys = ("id", "author", "text", "rating")
    quotes =  []
    for quote_db in quotes_db:
        quote = dict(zip(keys, quotes_db))
        quotes.append(quote)
    return jsonify(quotes), 200

@app.route("/params/<value>")
def param_example(value: str):
    return jsonify(param = value)

@app.route("/quotes/<int:quote_id>")
def get_quotes_by_id(quote_id:int)->dict:
    """функция возвращает цитату по значению ключа id=quote_id."""
    select_quote = "SELECT * FROM quotes WHERE id = ?"
    cursor = get_db().cursor
    quote_db = cursor.execute(select_quote(quote_id))
    if  quote_db:
        keys = ("id", "author", "text", "rating")
        quote = dict(zip(keys, quotes_db)).fetchone

    # for quote in   quotes:
    #     if quote["id"] == qute_id:
        return jsonify(quote), 200
    return {"error": f"quote with id= {qute_id} not found"}, 404

@app.get("/quotes/count")
def quotes_count():
    select_count = "SELECT count (*) as count FROM quotes"
    cursor = get_db().cursor
    cursor.execute(select_count)
    count = cursor.fetchone()
    if count:
        return jsonify(count = count[0]), 200
    abort(503) #вернем ошибку 503

# @app.route("/quotes/random", methods=["GET"])
# def random_quotes() -> dict:
#     return jsonify(choice(quotes))

@app.route("/quotes/filter")
def filter_quotes():
    filtered_quotes = quotes.copy()
    for key, value in request.args.items():
        if key not in ["author", "rating"]:
            return f"Invalid key{key}", HTTPStatus.BAD_REQUEST
        if key == "rating":
            value = int(value)
        filter_quotes =[
            quote
        for quote in filtered_quotes
        if quote[key] == value
        ]
    return filtered_quotes



# @app.route("/quotes", methods=['POST'])
# def create_quote():
#     new_qoute = request.json
#     new_id = last_quote["id"] +1
#     new_qoute["id"] = new_id
#     rating = new_qoute.get("rating")
#     if rating is None or rating not in range(1,6):
#         new_qoute["rating"] = 1
#     quotes.append(new_qoute)
#     return jsonify(new_qoute), 201


@app.route("/quotes", methods=['POST'])
def create_quote():
    new_quote = request.json
    insert_quote = "INSERT INTO quotes (author, text, rating) VALUES (?, ?, ?)"
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute(insert_quote, (new_quote['author'], new_quote['text'], new_quote['rating']))
    answer = cursor.lastrowid # Получаем из базы  id новой цитаты
    connection.commit()
    new_quote['id'] = answer
    return jsonify(new_quote), 201
    

@app.route("/quotes/<int:quote_id>", methods=["PUT"])
def edit_quote(quote_id):
    new_data = request.json
    if not set(new_data.keys()) - set("author", "rating", "text"):
        for quote in quotes:
            if quote["id"] == qute_id:
                if "rating" in new_data["rating"] not in range(1,6):
                    new_data.pop ("rating")
            quote.update(new_data)    
            return jsonify(quote), HTTPStatus.OK
    else:
            return {"error": "Send bad data to update"}, HTTPStatus.BAD_REQUEST
    return {"error": f"quote with id= {qute_id} not found"}, 404


@app.route("/quotes/<int:quote_id>", methods=["DELETE"])
def delete_quotes(quote_id:int):
    delete_sql = f"DELETE FROM quotes WHERE id =?"
    params = (quote_id,)
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute(delete_sql, params)
    rows = cursor.rowcount #Кол-во измененных строк
    if rows:
        connection.commit()
        cursor.close()
        return jsonify({"message": f"quote with id={quote_id} has deleted"}), 200
    connection.rollback()
    abort (404, f"quote with id= {qute_id} not found")

# @app.route("/quotes/filter")
# def filter_quotes():
# """TODO: change to work wuth database"""
#     filtered_quotes = quotes.copy()
#     for key, value in request.args.items():
#         if key not in ["author", "rating"]:
#             return f"Invalid key{key}", HTTPStatus.BAD_REQUEST
#         if key == "rating":
#             value = int(value)
#         filtered_quotes = [quote for quote in filter_quotes if quote.get[key] == value]
#         filtered_quotes = []
#         for quote in filter_quotes:
#             if quote[key] == value:
#                 filtered_quotes.append(quote)  
#     return filtered_quotes


if __name__ == "__main__":
    app.run(debug=True)