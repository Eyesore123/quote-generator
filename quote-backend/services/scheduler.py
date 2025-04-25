
from datetime import datetime # datetime module is used to work with dates and times.
from models import Subscriber
from data.quotes_data import quotes
from services.email_service import send_quote_email
import random

def send_quotes_by_schedule(frequency, current_hour):
    """
    Sends quotes to subscribers based on their preferred frequency and send hour.

    Args:
        frequency (str): The frequency of the quotes job (e.g. daily, weekly, monthly).
        current_hour (int): The current hour of the day.

    Returns:
        None
    """
    print(f"Running {frequency} quotes job at {datetime.now()}, hour: {current_hour}")
    try:
        subscribers = Subscriber.query.filter_by(frequency=frequency).all()
        for subscriber in subscribers:
            if subscriber.send_hour != current_hour:
                continue  # Only send to those who chose this hour

            categories = subscriber.categories.split(',') if subscriber.categories else []
            filtered_quotes = [quote for quote in quotes if not categories or quote['author'] in categories]

            if filtered_quotes:
                random_quote = random.choice(filtered_quotes)
                send_quote_email(
                    subscriber.email, 
                    random_quote['quote'], 
                    random_quote['author'], 
                    None  # No category available in the quotes data
                )
    except Exception as e:
        print(f"Error in {frequency} quotes job: {e}")