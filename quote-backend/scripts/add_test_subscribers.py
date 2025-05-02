from models import Subscriber, db
from app import app

with app.app_context():
    send_hour = 9

    s1 = Subscriber(email='test_daily@example.com', send_hour=send_hour, categories='philosophy', time_zone='Europe/London', frequency='weekly')
    s2 = Subscriber(email='test_weekly@example.com', send_hour=send_hour, categories='philosophy', time_zone='Europe/London', frequency='monthly')
    s3 = Subscriber(email='test_monthly@example.com', send_hour=send_hour, categories='philosophy', time_zone='Europe/Helsinki', frequency='daily')

    db.session.add_all([s1, s2, s3])
    db.session.commit()

    print("Test subscribers added successfully.")

    # Run with: python scripts/add_test_subscribers.py, then check the database