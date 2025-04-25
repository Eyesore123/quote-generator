import smtplib # simple mail transfer protocol module
import os # operating system
from email.mime.text import MIMEText    # MIME (Multipurpose Internet Mail Extensions) is a standard for formatting email messages.
from email.mime.multipart import MIMEMultipart # MIMEMultipart is a class that represents a MIME multipart message.

# send email function, first msg object, then smtplib:

def send_email(to_email, subject, body):

    from_email = os.environ.get("EMAIL_USERNAME")
    password = os.environ.get("EMAIL_PASSWORD")

    if not from_email or not password:
        print("Email credentials not found in environment variables. Skipping email sending.")
        return
    
    # message object

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    # send email

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        server.send_message(msg)
        server.quit()
        print(f"Email sent to {to_email}")
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