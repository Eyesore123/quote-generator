from flask import Blueprint, jsonify, request
from models import db, Subscriber
from data.quotes_data import quotes

subscription_routes = Blueprint('subscription_routes', __name__)

# === GET all matching quotes by query ===
@subscription_routes.route('/api/search', methods=['GET'])
def search_quotes():
    query = request.args.get('q', '').lower()
    results = []

    for category, quote_list in quotes.items():
        for quote in quote_list:
            if query in quote["quote"].lower() or query in quote["author"].lower():
                results.append({
                    "quote": quote["quote"],
                    "author": quote["author"],
                    "category": category
                })

    return jsonify({
        "success": True,
        "count": len(results),
        "quotes": results
    })


# === POST: Subscribe via email ===
@subscription_routes.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')
    send_hour = request.form.get('send_hour')
    categories = request.form.getlist('categories')
    if not email:
        return jsonify({"message": "Email is required."}), 400
    if not send_hour:
        return jsonify({"message": "Send hour is required."}), 400

    existing = Subscriber.query.filter_by(email=email).first()
    if existing:
        return jsonify({"message": "You are already subscribed to our newsletter."}), 200

    new_subscriber = Subscriber(email=email, send_hour=send_hour, categories=categories)
    db.session.add(new_subscriber)
    db.session.commit()
    return jsonify({"message": "You have successfully subscribed to our newsletter!"}), 201

# === POST: Unsubscribe via email ===
@subscription_routes.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    email = request.form.get('email')
    if not email:
        return jsonify({"message": "Email is required."}), 400

    subscriber = Subscriber.query.filter_by(email=email).first()
    if subscriber:
        db.session.delete(subscriber)
        db.session.commit()
        return jsonify({"message": "Unsubscribed successfully."})
    else:
        return jsonify({"message": "You were not subscribed to our newsletter."}), 200


# === GET: List quote categories ===
@subscription_routes.route('/api/quotes/categories', methods=['GET'])
def get_categories():
    try:
        categories = list(quotes.keys())
        return jsonify({
            'success': True,
            'categories': categories
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
