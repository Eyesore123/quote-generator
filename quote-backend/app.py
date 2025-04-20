from flask import Flask, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)

CORS(app)

quotes = {
    "philosophy": [
        "The unexamined life is not worth living. — Socrates",
        "I think, therefore I am. — Descartes",
        "He who thinks great thoughts, often makes great errors. — Heidegger"
    ],
    "humor": [
        "I'm not arguing, I'm just explaining why I'm right.",
        "I'm on a whiskey diet. I've lost three days already.",
        "Why don’t scientists trust atoms? Because they make up everything!"
    ],
    "random": [
        "Be yourself; everyone else is already taken. — Oscar Wilde",
        "You only live once, but if you do it right, once is enough. — Mae West",
        "In the middle of difficulty lies opportunity. — Einstein"
    ]
}

@app.route('/quote/<category>')
def get_route(category):
    category_quotes = quotes.get(category, quotes["random"])
    return jsonify({"quote": random.choice(category_quotes)})

@app.route('/')
def hello():
    return 'Quote API is running!'

if __name__ == '__main__':
    app.run(debug=True)