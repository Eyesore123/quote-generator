# This script is used to delete subscribers from the database based on their email or send_hour.
# Runs the script with specified commands.
# Delete by email: python delete_subscribers.py email <email_address>
# Delete by send_hour: python delete_subscribers.py send_hour <hour_value>

import sys
from models import Subscriber, db
from app import create_app
# Initialize the Flask app
app = create_app()

def delete_subscriber_by_email(email):
    """Delete a subscriber by their email address."""
    with app.app_context():
        subscriber = Subscriber.query.filter_by(email=email).first()
        if subscriber:
            db.session.delete(subscriber)
            db.session.commit()
            print(f"Subscriber with email {email} deleted successfully.")
        else:
            print(f"No subscriber found with email: {email}")

def delete_subscribers_by_hour(send_hour):
    """Delete subscribers that have a specific send_hour."""
    with app.app_context():
        subscribers = Subscriber.query.filter_by(send_hour=send_hour).all()
        if subscribers:
            for subscriber in subscribers:
                db.session.delete(subscriber)
            db.session.commit()
            print(f"Deleted {len(subscribers)} subscribers with send_hour = {send_hour}")
        else:
            print(f"No subscribers found with send_hour: {send_hour}")

if __name__ == '__main__':
    # Command-line arguments to specify the operation
    if len(sys.argv) < 3:
        print("Usage: python delete_subscribers.py [email|send_hour] [value]")
        sys.exit(1)

    param = sys.argv[1].lower()
    value = sys.argv[2]

    if param == "email":
        delete_subscriber_by_email(value)
    elif param == "send_hour":
        try:
            send_hour = int(value)
            delete_subscribers_by_hour(send_hour)
        except ValueError:
            print("Invalid send_hour value. It should be an integer.")
    else:
        print("Invalid parameter. Use 'email' or 'send_hour'.")
