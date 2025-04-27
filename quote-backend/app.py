from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from services.scheduler import start_scheduler
import os
from models import db
from dotenv import load_dotenv
from services.scheduler import start_scheduler

load_dotenv()

# Import the quotes dictionary from quotes_data.py
from data.quotes_data import quotes

# from config import Config
from routes.subscription_routes import subscription_routes
# from models import Quote
import random

# Initialize sql alchemy in here + import migrate

app = Flask(__name__)
CORS(app, origins="*")

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

start_scheduler(app)

if __name__ == "__main__":
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        start_scheduler(app)

    app.run(debug=False, use_reloader=False)