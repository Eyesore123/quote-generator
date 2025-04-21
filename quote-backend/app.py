from flask import Flask, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)

CORS(app, origins="*")

# quotes = {
#     "philosophy": [
#         "The unexamined life is not worth living. — Socrates",
#         "I think, therefore I am. — Descartes",
#         "He who thinks great thoughts, often makes great errors. — Heidegger"
#     ],
#     "humor": [
#         "I'm not arguing, I'm just explaining why I'm right.",
#         "I'm on a whiskey diet. I've lost three days already.",
#         "Why don’t scientists trust atoms? Because they make up everything!"
#     ],
#     "random": [
#         "Be yourself; everyone else is already taken. — Oscar Wilde",
#         "You only live once, but if you do it right, once is enough. — Mae West",
#         "In the middle of difficulty lies opportunity. — Einstein"
#     ]
# }

# New upcoming quote structure:

quotes = {
    "philosophy": [
        {"quote": "The unexamined life is not worth living.", "author": "Socrates"},
        {"quote": "I think, therefore I am.", "author": "Descartes"},
        {"quote": "He who thinks great thoughts, often makes great errors.", "author": "Heidegger"}
    ],
    "humor": [
        {"quote": "I'm not arguing, I'm just explaining why I'm right.", "author": "Unknown"},
        {"quote": "I'm on a whiskey diet. I've lost three days already.", "author": "Unknown"},
        {"quote": "Why don’t scientists trust atoms? Because they make up everything!", "author": "Unknown"}
    ],
    "random": [
        {"quote": "Be yourself; everyone else is already taken.", "author": "Oscar Wilde"},
        {"quote": "You only live once, but if you do it right, once is enough.", "author": "Mae West"},
        {"quote": "In the middle of difficulty lies opportunity.", "author": "Einstein"}
    ]
}


@app.route('/quote/<category>')
def get_route(category):
    category_quotes = quotes.get(category, quotes["random"])
    return jsonify({"quote": random.choice(category_quotes)})

@app.route('/quotes')
def get_all_quotes():
    all_quotes = []
    for category, items in quotes.items():
        for q in items:
            all_quotes.append({**q, "category": category})
    return jsonify(all_quotes)

if __name__ == '__main__':
    app.run(debug=True)