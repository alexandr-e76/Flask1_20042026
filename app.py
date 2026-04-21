from flask import Flask, jsonify, request
from typing import Any
from random import choice

app = Flask(__name__)

about_me = {
    "name": "Александр",
    "surname": "Егоров",
    'email': "egorov1011@gmail.com"
}
quotes = [
{
"id": 3,
"author": "Rick Cook",
"text": """Программирование сегодня — это гонка разработчиков программ, стремящихся писать программы с
большей и лучшей идиотоустойчивостью, и вселенной, которая
пытается создать больше отборных идиотов. Пока вселенная
побеждает."""
},
{
"id": 5,
"author": "Waldi Ravens",
"text": "Программирование на С похоже на быстрые танцы \
на только что отполированном полу людей с острыми бритвами в \
руках."
},
{
"id": 6,
"author": "Mosher’s Law of Software Engineering",
"text": "Не волнуйтесь, если что-то не работает. Если \
бы всё работало, вас бы уволили."
},
{
"id": 8,
"author": "Yoggi Berra",
"text": "В теории, теория и практика неразделимы. На \
практике это не так."
},
]
# Нужно больше цитат? https://tproger.ru/devnull/programming-quotes/По url: /quotes , вернем полный список цитат
@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route("/about")
def about():
    return about_me

@app.route("/quotes")
def get_quotes()->list[dict[str, any]]:
    return quotes

app.route("/params/<value>")
def param_example(value: str):
    return jsonify(param = value)

@app.route("/quotes/<int:quote_id>")
def get_quotes_by_id(quote_id:int)->dict:
    for quote in   quotes:
        if quote["id"] == qute_id:
            return jsonify(quote), 200
    return {"error": f"quote with id= {qute_id} not found"}, 404

app.get("/quotes/count")
def quotes_count():
    return jsonify(count = len(quotes))

@app.route("/quotes/random", methods=["GET"])
def random_quotes() -> dict:
    return jsonify(choice(quotes))

@app.route("/quotes", methods=['POST'])
def create_quote():
    new_qoute = request.json
    new_id = last_quote["id"] +1
    new_qoute["id"] = new_id
    quotes.append(new_qoute)
    return jsonify(new_qoute), 201

@app.route("/quotes/<int:quote_id>", methods=["DELETE"])
def get_quotes_by_id(quote_id:int):
    for quote in   quotes:
        if quote["id"] == qute_id:
            quotes.remove(quote)
            return jsonify({"message": f"quote with id={quote_id} has deleted"}), 200
    return {"error": f"quote with id= {qute_id} not found"}, 404


if __name__ == "__main__":
    app.run(debug=True)