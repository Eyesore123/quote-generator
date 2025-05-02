# This script is used to trigger the email sending process for testing purposes without waiting for the scheduled time. Make sure your env variables are set correctly.

from services.scheduler import send_quotes_at_hour

if __name__ == '__main__':
    send_quotes_at_hour()

    # Run with: python trigger_email_test.py
