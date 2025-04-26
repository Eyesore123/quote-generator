import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# send email function, first msg object, then smtplib:

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email(to_email, subject, body):
    api_key = os.environ.get("SENDGRID_API_KEY")
    from_email = os.environ.get("EMAIL_USERNAME")  # Use the same from email you verified in SendGrid

    if not api_key or not from_email:
        print("SendGrid credentials not found. Skipping email sending.")
        return

    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        plain_text_content=body
    )

    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        print(f"Email sent to {to_email}. Status Code: {response.status_code}")
    except Exception as e:
        print(f"Error sending email to {to_email}: {e}")


# Welcome email function

def send_welcome_email(email):
    subject = "Welcome to Quote Generator Subscription!"
    body = """
    Thank you for subscribing to our quote service!

    You'll receive quotes based on your preferences.

    If you wish to unsubscribe at any time, please visit our website.

    Best regards,
    The  Quote Generator Team
    """
    send_email(email, subject, body)

# Quote email function

def send_quote_email(email, quote, author, category=None):
    category_text = f"Your {category.capitalize()} Quote" if category else "A Random Quote"
    subject = category_text
    body = f'"{quote}"\n\n—{author}'
    send_email(email, subject, body)