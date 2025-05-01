import threading
from datetime import datetime
from models import Subscriber, db
from data.quotes_data import quotes
from services.email_service import send_quote_email
import random
import schedule
import time
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

    if scheduler_running:
        print("Scheduler is already running. Skipping this job.")
        return

    scheduler_running = True

    try:
        now_utc = datetime.utcnow()
        print(f"Running job at UTC hour {now_utc.hour} at {now_utc}")

        with app.app_context():
            subscribers = db.session.query(Subscriber).all()

            for subscriber in subscribers:
                try:
                    user_tz = pytz.timezone(subscriber.time_zone)
                except UnknownTimeZoneError:
                    print(f"Unknown timezone for {subscriber.email}: {subscriber.time_zone}")
                    continue

                user_now = datetime.now(user_tz)
                user_current_hour = user_now.hour

                if user_current_hour != subscriber.send_hour:
                    continue

                if subscriber.frequency not in ['daily', 'weekly', 'monthly']:
                    continue

                if subscriber.frequency == 'weekly' and user_now.weekday() != 0:  # Monday only
                    continue

                if subscriber.frequency == 'monthly' and user_now.day != 1:  # 1st day only
                    continue

                all_quotes = []
                for quote_list in quotes.values():
                    all_quotes.extend(quote_list)

                random_quote = random.choice(all_quotes)
                quote_text = random_quote['quote']
                author = random_quote['author']

                send_quote_email(subscriber.email, quote_text, author)

                print(f"Sent quote to {subscriber.email} at their local hour {user_current_hour} ({subscriber.time_zone})")

    except Exception as e:
        print(f"Error sending quotes: {e}")

    finally:
        scheduler_running = False


def start_scheduler(app):
    print(threading.current_thread().name)
    # Ensure the job is scheduled only once
    if not scheduler_lock.locked():
        scheduler_lock.acquire()
        try:
            if scheduler_running:
                print("Scheduler already running, skipping start.")
                return

            schedule.clear("send_quotes_at_hour")  # Clear any previously scheduled jobs
            # Schedule job to run every hour, send first immediately
            schedule.every().hour.do(send_quotes_at_hour, app).tag("send_quotes_at_hour")
            send_quotes_at_hour(app)

            print("Scheduler started, will run every hour at :00")
        finally:
            scheduler_lock.release()

    # Start a background thread to run the scheduler
    def run_scheduler():
        while True:
            schedule.run_pending()  # Run any scheduled jobs
            time.sleep(1)

    # Start the scheduler in a new daemon thread
    threading.Thread(target=run_scheduler, daemon=False).start()
