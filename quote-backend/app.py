from flask import Flask, jsonify, send_from_directory
from flask_migrate import Migrate
from flask_cors import CORS
from services.scheduler import start_scheduler
import os
import logging
from logging.handlers import RotatingFileHandler
from models import db
from dotenv import load_dotenv
from services.scheduler import start_scheduler
from waitress import serve

load_dotenv()

# Import the quotes dictionary from quotes_data.py
from data.quotes_data import quotes

# from config import Config
from routes.subscription_routes import subscription_routes
# from models import Quote
import random

# Create a logger

if not os.path.exists('logs'):
    os.mkdir('logs')

file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=2)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)

# Initialize sql alchemy in here + import migrate

app = Flask(__name__)
CORS(app, origins="*")

app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('Quote backend startup')

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

# Register the subscription routes blueprint

app.register_blueprint(subscription_routes)

# Duplicate finder func:
all_quotes = []
for category, category_quotes in quotes.items():
    for q in category_quotes:
        if (q['quote'], q['author']) in all_quotes:
            print(f"Duplicate found: {q['quote']} by {q['author']}")  # Print duplicates
        else:
            all_quotes.append((q['quote'], q['author']))

# Calculate the number of quotes in each category

quote_counts = {category: len(quotes) for category, quotes in quotes.items()}
print(quote_counts)

# Calculate total amount of quotes

total_quotes = sum(quote_counts.values())
print(f"Total number of quotes: {total_quotes}")

@app.route('/')
def home():
    return 'Backend is running!'


# Route for getting a random quote, not in use

@app.route('/quote/<category>')
def get_route(category):
    if category == "all":
        all_quotes = [q for quotes_list in quotes.values() for q in quotes_list]
        return jsonify({"quote": random.choice(all_quotes)})
    else:
        category_quotes = quotes.get(category, quotes["random"])
        return jsonify({"quote": random.choice(category_quotes)})

# Route for getting all quotes

@app.route('/quotes')
def get_all_quotes():
    all_quotes = []
    for category, items in quotes.items():
        for q in items:
            all_quotes.append({**q, "category": category})
    return jsonify(all_quotes)

# Serve the Angular app's index.html file for all routes

@app.route('/<path:path>')
def catch_all(path):
    return send_from_directory('dist/quote-app', path)

# Gunicorn does not call __main__, so no need to call it inside if statement when using that. This setup is for Waitress:
# if __name__ == "__main__":
#     start_scheduler(app)
#     serve(app, host="0.0.0.0", port=5000)


# This is for Gunicorn:

start_scheduler(app)

if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)
