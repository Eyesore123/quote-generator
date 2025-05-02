from flask import Blueprint, jsonify
from services.scheduler import send_quotes_at_hour
from flask import current_app
from datetime import datetime

scheduler_routes = Blueprint('scheduler_routes', __name__)

@scheduler_routes.route('/trigger-send-quote', methods=['GET'])
def trigger_send_quote():
    print(f"[{datetime.now()}] /trigger-send-quote route HIT — Manually triggering send_quotes_at_hour()")
    send_quotes_at_hour(current_app._get_current_object())
    return jsonify({"message": "Quote email sent successfully"})
