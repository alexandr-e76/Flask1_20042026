from flask import Flask, jsonify, request
from typing import Any
from random import choice
from http import HTTPStatus
from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).parent
path_to_db = BASE_DIR / "store.db" # <- тут путь к БД
# Используем так:
connection = sqlite3.connect(path_to_db)

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

about_me = {
    "name": "Александр",
    "surname": "Егоров",
    'email': "egorov1011@gmail.com"
}
# quotes = [
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
@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route("/about")
def about():
    return about_me

@app.route("/quotes")
def get_quotes()->list[dict[str, any]]:
    select_quotes = "SELECT * from quotes"

# Подключение в БД
    connection = sqlite3.connect("store.db")
# Создаем cursor, он позволяет делать SQL-запросы
    cursor = connection.cursor()
# Выполняем запрос:
    cursor.execute(select_quotes)
# Извлекаем результаты запроса
    quotes_db = cursor.fetchall() # Здесь получаем список кортежей
    print(f"{quotes_db =}")
# Закрыть курсор:
    cursor.close()
# Закрыть соединение:
    connection.close()
#Поготовка данных для отправки в праильном формате
#Необходимо выполнить преобразование:
#list[tuple] -> list[dict]
    keys = ("id", "author", "text")
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
    for quote in   quotes:
        if quote["id"] == qute_id:
            return jsonify(quote), 200
    return {"error": f"quote with id= {qute_id} not found"}, 404

@app.get("/quotes/count")
def quotes_count():
    return jsonify(count = len(quotes))

@app.route("/quotes/random", methods=["GET"])
def random_quotes() -> dict:
    return jsonify(choice(quotes))

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



@app.route("/quotes", methods=['POST'])
def create_quote():
    new_qoute = request.json
    new_id = last_quote["id"] +1
    new_qoute["id"] = new_id
    rating = new_qoute.get("rating")
    if rating is None or rating not in range(1,6):
        new_qoute["rating"] = 1
    quotes.append(new_qoute)
    return jsonify(new_qoute), 201

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


#@app.route("/quotes/<int:quote_id>", methods=["DELETE"])
#def get_quotes_by_id(quote_id:int):
#    for quote in   quotes:
#       if quote["id"] == qute_id:
#            quotes.remove(quote)
#            return jsonify({"message": f"quote with id={quote_id} has deleted"}), 200
#    return {"error": f"quote with id= {qute_id} not found"}, 404

# @app.route("/quotes/filter")
# def filter_quotes():
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