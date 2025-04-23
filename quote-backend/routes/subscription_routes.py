from flask import Blueprint, jsonify, request
from models import Quote # Import the Quote class from models.py

# Blueprint for subscription routes

subscription_routes = Blueprint('subscription_routes', __name__)

# Route for subscribing to a quote via form

subscribers = []

@subscription_routes.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form('email')
    if email not in subscribers:
        subscribers.append(email)
        return jsonify({"message": "You have successfully subscribed to our newsletter!"})
    else:
        return jsonify({"message": "You are already subscribed to our newsletter."})
    
