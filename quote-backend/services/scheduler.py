from datetime import datetime
from models import Subscriber, db
from data.quotes_data import quotes
from services.email_service import send_quote_email
import random
import schedule
import time
import threading

def send_quotes_at_hour(app):
    now = datetime.now()
    current_hour = now.hour

    print(f"Running job for hour {current_hour} at {now}")

    try:
        with app.app_context():
            subscribers = db.session.query(Subscriber).filter(Subscriber.send_hour == current_hour).all()

            for subscriber in subscribers:
                if subscriber.frequency not in ['daily', 'weekly', 'monthly']:
                    continue

                if subscriber.frequency == 'weekly' and now.weekday() != 0:  # Monday only
                    continue

                if subscriber.frequency == 'monthly' and now.day != 1:  # 1st day only
                    continue

                all_quotes = []
                for quote_list in quotes.values():
                    all_quotes.extend(quote_list)

                random_quote = random.choice(all_quotes)

                quote_text = random_quote['quote']
                author = random_quote['author']

                send_quote_email(subscriber.email, quote_text, author)

                print(f"Sent quote to {subscriber.email} at {now}")

    except Exception as e:
        print(f"Error sending quotes at hour {current_hour}: {e}")


def start_scheduler(app):
    # Run every hour at :00 minutes
    schedule.every().hour.at(":00").do(send_quotes_at_hour, app)

    print("Scheduler started, will run every hour at :00")

    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(1)

    threading.Thread(target=run_scheduler, daemon=True).start()

