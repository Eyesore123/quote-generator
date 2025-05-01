# app.py

from flask import Flask, jsonify, send_from_directory, redirect
from flask_migrate import Migrate
from flask_cors import CORS
from services.scheduler import start_scheduler
from models import db
from routes.subscription_routes import subscription_routes
from dotenv import load_dotenv
from waitress import serve
import os
import logging
from logging.handlers import RotatingFileHandler
import random

# Load environment variables
load_dotenv()

# === Initialize app and config ===
app = Flask(__name__, static_folder='dist/quote-app')
CORS(app, origins="*")

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

# === Logger setup ===
if not os.path.exists('logs'):
    os.mkdir('logs')

file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=2)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)

app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('Quote backend startup')

# === Import quotes data ===
from data.quotes_data import quotes

# === Register Blueprints ===
app.register_blueprint(subscription_routes)

# === Debugging helpers (quote counts + duplicates) ===
all_quotes_check = []
for category, category_quotes in quotes.items():
    for q in category_quotes:
        if (q['quote'], q['author']) in all_quotes_check:
            print(f"Duplicate found: {q['quote']} by {q['author']}")
        else:
            all_quotes_check.append((q['quote'], q['author']))

quote_counts = {category: len(quotes_list) for category, quotes_list in quotes.items()}
print(quote_counts)

total_quotes = sum(quote_counts.values())
print(f"Total number of quotes: {total_quotes}")

# === API routes ===
@app.route('/')
def home():
    return 'Backend is running!'

@app.route('/quote/<category>')
def get_route(category):
    if category == "all":
        all_quotes = [q for quotes_list in quotes.values() for q in quotes_list]
        return jsonify({"quote": random.choice(all_quotes)})
    else:
        category_quotes = quotes.get(category, quotes["random"])
        return jsonify({"quote": random.choice(category_quotes)})

@app.route('/quotes')
def get_all_quotes():
    all_quotes = []
    for category, items in quotes.items():
        for q in items:
            all_quotes.append({**q, "category": category})
    return jsonify(all_quotes)

# === Serve Angular app for all frontend routes ===@app.route('/', defaults={'path': ''})
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    file_path = os.path.join(app.static_folder, path)

    if path != "" and os.path.exists(file_path) and os.path.isfile(file_path):
        return send_from_directory(app.static_folder, path)
    else:
        # Serve index.html for Angular routes like /unsubscribed, /search, etc.
        return send_from_directory(app.static_folder, 'index.html')


# === Start scheduler ===
start_scheduler(app)

# === Server startup ===
if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)
    # If using Waitress in production, uncomment this instead:
    # serve(app, host="0.0.0.0", port=5000)
