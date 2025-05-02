import threading
from datetime import datetime
from models import Subscriber, db
from data.quotes_data import quotes
from services.email_service import send_quote_email
import random
import schedule
import time
from datetime import timezone, datetime, timedelta
import pytz
from pytz.exceptions import UnknownTimeZoneError

# Note: The logging setup is commented out for simplicity. You can uncomment and configure it as needed.
# import logging 
# Initialize the logger
# logger = logging.getLogger(__name__)
# Then use logger like "logger.info('Your message') or logger.error('Your message')"

# A global lock to ensure only one scheduler thread runs
scheduler_lock = threading.Lock()

# To store if the scheduler is already running
scheduler_running = False

def send_quotes_at_hour(app):
    global scheduler_running

    now_utc = datetime.now(timezone.utc)
    finland_time = now_utc + timedelta(hours=3)
    current_hour = finland_time.hour

    print(f"[{now_utc}] Triggered send_quotes_at_hour() — Finland local hour: {current_hour} (UTC hour: {now_utc.hour})")

    if scheduler_running:
        print(f"[{now_utc}] Scheduler is already running. Skipping this job.")
        return

    scheduler_running = True

    try:
        with app.app_context():
            subscribers = db.session.query(Subscriber).filter(Subscriber.send_hour == current_hour).all()

            print(f"[{now_utc}] Fetched {len(subscribers)} subscribers with send_hour = {current_hour}")

            for subscriber in subscribers:
                print(f"[{now_utc}] Checking subscriber {subscriber.email} — frequency: {subscriber.frequency}")

                if subscriber.frequency not in ['daily', 'weekly', 'monthly']:
                    print(f"[{now_utc}] Skipping {subscriber.email} — invalid frequency: {subscriber.frequency}")
                    continue

                if subscriber.frequency == 'weekly' and now_utc.weekday() != 0:
                    print(f"[{now_utc}] Skipping {subscriber.email} — today is not Monday")
                    continue

                if subscriber.frequency == 'monthly' and now_utc.day != 1:
                    print(f"[{now_utc}] Skipping {subscriber.email} — today is not 1st of month")
                    continue

                all_quotes = []
                for quote_list in quotes.values():
                    all_quotes.extend(quote_list)

                random_quote = random.choice(all_quotes)
                quote_text = random_quote['quote']
                author = random_quote['author']

                send_quote_email(subscriber.email, quote_text, author)
                print(f"[{now_utc}] Sent quote to {subscriber.email}")

    except Exception as e:
        print(f"[{now_utc}] Error sending quotes at hour {current_hour}: {e}")

    finally:
        scheduler_running = False
        print(f"[{now_utc}] Finished send_quotes_at_hour()")


def start_scheduler(app):
    print(f"[{datetime.now()}] MainThread — Starting scheduler")

    if not scheduler_lock.locked():
        scheduler_lock.acquire()
        try:
            if scheduler_running:
                print(f"[{datetime.now()}] Scheduler already running, skipping start.")
                return

            schedule.clear("send_quotes_at_hour")
            schedule.every().hour.do(send_quotes_at_hour, app).tag("send_quotes_at_hour")
            print(f"[{datetime.now()}] Scheduled send_quotes_at_hour() to run every hour")
            
            # Trigger first run immediately
            send_quotes_at_hour(app)

        finally:
            scheduler_lock.release()

    def run_scheduler():
        print(f"[{datetime.now()}] Scheduler background thread started")
        while True:
            schedule.run_pending()
            time.sleep(1)

    threading.Thread(target=run_scheduler, daemon=False).start()

