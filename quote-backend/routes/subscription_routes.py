from flask import Blueprint, jsonify, request
from flask import redirect
from models import db, Subscriber
from data.quotes_data import quotes
from services.email_service import send_welcome_email

subscription_routes = Blueprint('subscription_routes', __name__)

# === GET: Search quotes ===
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
    data = request.get_json()
    email = data.get('email')
    send_hour = data.get('send_hour')
    frequency = data.get('frequency', 'daily')
    categories = data.get('categories', '')
    time_zone = data.get('time_zone', 'UTC')

    if not email:
        return jsonify({"message": "Email is required."}), 400
    if send_hour is None:
        return jsonify({"message": "Send hour is required."}), 400

    subscriber = Subscriber.query.filter_by(email=email).first()
    if subscriber:
        # Update existing subscriber
        subscriber.send_hour = send_hour
        subscriber.frequency = frequency
        subscriber.categories = categories
        subscriber.time_zone = time_zone
        db.session.commit()
        return jsonify({"message": "Subscription updated!"}), 200

    # Create new subscriber
    new_subscriber = Subscriber(
        email=email,
        send_hour=send_hour,
        frequency=frequency,
        categories=categories,
        time_zone=time_zone
    )
    db.session.add(new_subscriber)
    db.session.commit()
    send_welcome_email(email)
    return jsonify({"message": "You have successfully subscribed to our newsletter!"}), 201

# === Handles both GET (via link) and POST (via form) to unsubscribe ===
@subscription_routes.route('/unsubscribe', methods=['GET', 'POST'])
def unsubscribe():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
    else:  # GET method
        email = request.args.get('email')

    if not email:
        if request.method == 'POST':
            return jsonify({"message": "Email is required."}), 400
        else:
            # Redirect anyway to confirmation page for cleaner UX
            return redirect('https://myquoteapp1.netlify.app/unsubscribed')

    subscriber = Subscriber.query.filter_by(email=email).first()
    if subscriber:
        db.session.delete(subscriber)
        db.session.commit()

    # Whether they were subscribed or not, we redirect/confirm
    if request.method == 'POST':
        return jsonify({"message": "You have been unsubscribed successfully."}), 200
    else:
        return redirect('https://myquoteapp1.netlify.app/unsubscribed')

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
