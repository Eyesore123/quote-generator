from datetime import datetime
from models import Subscriber, db
from data.quotes_data import quotes
from services.email_service import send_quote_email
import random
import schedule
import time
import threading

def send_quotes_at_hour(hour):
    print(f"Running job for hour {hour} at {datetime.now()}")

    try:
        subscribers = db.session.query(Subscriber).filter(Subscriber.send_hour == hour).all()

        for subscriber in subscribers:
            # Optional: filter by frequency too
            if subscriber.frequency not in ['daily', 'weekly', 'monthly']:
                continue

            if subscriber.frequency == 'weekly' and datetime.now().weekday() != 0:  # Only on Mondays
                continue

            if subscriber.frequency == 'monthly' and datetime.now().day != 1:  # Only on the 1st of the month
                continue

            random_quote = random.choice(quotes)
            send_quote_email(subscriber.email, random_quote)

    except Exception as e:
        print(f"Error sending quotes at hour {hour}: {e}")

def start_scheduler():
    for hour in range(24):  # Schedule job for every hour
        schedule.every().day.at(f"{hour:02d}:00").do(send_quotes_at_hour, hour)

    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(60)

    threading.Thread(target=run_scheduler, daemon=True).start()
    print("Dynamic scheduler started")

# Call this once when app starts
start_scheduler()
