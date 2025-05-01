from flask import Blueprint, jsonify
from services.scheduler import send_quotes_at_hour

scheduler_routes = Blueprint('scheduler_routes', __name__)

@scheduler_routes.route('/trigger-send-quote', methods=['GET'])
def trigger_send_quote():
    send_quotes_at_hour(None)
    return jsonify({"message": "Quote email sent successfully"})
