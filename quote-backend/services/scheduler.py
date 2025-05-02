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

# A global lock to ensure only one scheduler thread runs
scheduler_lock = threading.Lock()

# To store if the scheduler is already running
scheduler_running = False

def send_quotes_at_hour(app):
    global scheduler_running

    now_utc = datetime.now(pytz.utc)

    print(f"[{now_utc}] Triggered send_quotes_at_hour() — Current UTC hour: {now_utc.hour}")

    if scheduler_running:
        print(f"[{now_utc}] Scheduler is already running. Skipping this job.")
        return

    scheduler_running = True

    try:
        with app.app_context():
            subscribers = Subscriber.query.all()

            print(f"[{now_utc}] Fetched {len(subscribers)} total subscribers")

            sent_count = 0

            for subscriber in subscribers:
                try:
                    user_tz = pytz.timezone(subscriber.time_zone)
                    now_user_time = now_utc.astimezone(user_tz)

                    if now_user_time.hour != subscriber.send_hour:
                        continue  # Skip if not their chosen hour

                    print(f"[{now_utc}] Checking subscriber {subscriber.email} — "
                          f"Local hour {now_user_time.hour} "
                          f"(timezone: {subscriber.time_zone}) — frequency: {subscriber.frequency}")

                    # Validate frequency rules
                    if subscriber.frequency not in ['daily', 'weekly', 'monthly']:
                        print(f"[{now_utc}] Skipping {subscriber.email} — invalid frequency: {subscriber.frequency}")
                        continue

                    if subscriber.frequency == 'weekly' and now_user_time.weekday() != 0:
                        print(f"[{now_utc}] Skipping {subscriber.email} — today is not Monday")
                        continue

                    if subscriber.frequency == 'monthly' and now_user_time.day != 1:
                        print(f"[{now_utc}] Skipping {subscriber.email} — today is not 1st of month")
                        continue

                    # Gather and send random quote from selected categories
                    selected_categories = subscriber.categories.split(',')
                    selected_quotes = []

                    for category in selected_categories:
                        category = category.strip()
                        if category in quotes:
                            selected_quotes.extend(quotes[category])

                    if not selected_quotes:
                        print(f"[{now_utc}] Skipping {subscriber.email} — no valid quotes in selected categories")
                        continue

                    random_quote = random.choice(selected_quotes)
                    quote_text = random_quote['quote']
                    author = random_quote['author']

                    send_quote_email(subscriber.email, quote_text, author)
                    print(f"[{now_utc}] ✅ Sent quote to {subscriber.email}")

                    sent_count += 1

                except UnknownTimeZoneError:
                    print(f"[{now_utc}] ⚠️ Skipping {subscriber.email} — Invalid timezone: {subscriber.time_zone}")

    except Exception as e:
        print(f"[{now_utc}] ❌ Error sending quotes: {e}")

    finally:
        scheduler_running = False
        print(f"[{now_utc}] Finished send_quotes_at_hour() — Emails sent: {sent_count}")


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
