import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# send email function, first msg object, then smtplib:

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email(to_email, subject, plain_body, html_body=None):
    api_key = os.environ.get("SENDGRID_API_KEY")
    from_email = os.environ.get("EMAIL_USERNAME")  # Use the same from email you verified in SendGrid

    if not api_key or not from_email:
        print("SendGrid credentials not found. Skipping email sending.")
        return

    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        plain_text_content=plain_body,
        html_content=html_body or plain_body  # Fallback to plain text if HTML is not provided
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
    plain_body = """
    Thank you for subscribing to our quote service!

    You'll receive quotes based on your preferences.

    If you wish to unsubscribe at any time, please visit our website.

    Best regards,
    The Quote Generator Team
    """

    backend_url = "https://quote-app-backend-nk7c.onrender.com"
    unsubscribe_link = f"{backend_url}/unsubscribe?email={email}"

    html_body = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; color: #333;">
            <h2 style="color: #2c3e50;">Welcome to Quote Generator!</h2>
            <p style="font-size: 16px;">
                Thank you for subscribing to our quote service!<br><br>
                You'll soon start receiving inspiring quotes based on your preferences.<br><br>
                If you wish to unsubscribe at any time, please click <a href="{unsubscribe_link}" style="color: #2980b9;">here</a>.
            </p>
            <hr style="border: 1px solid #ccc; margin: 20px 0;">
            <p style="font-size: 0.9em;">
                Best regards,<br>
                The Quote Generator Team
            </p>
        </div>
    """

    send_email(email, subject, plain_body, html_body)


# Quote email function

def send_quote_email(email, quote, author, category=None):
    category_text = f"Your {category.capitalize()} Quote 🌟" if category else "A Random Quote 🌟"
    subject = category_text
    plain_body = f'"{quote}"\n\n—{author}'

    backend_urL = "https://quote-app-backend-nk7c.onrender.com"
    unsubscribe_link = f"{backend_urL}/unsubscribe?email={email}"

    html_body = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; color: #333;">
            <h2 style="color: #2c3e50;">{category_text}</h2>
            <blockquote style="font-style: italic; color: #555;">
                <p style="font-size: 18px;">"{quote}"</p>
                <br><strong>—{author}</strong>
            </blockquote>
            <hr style="border: 1px solid #ccc; margin: 20px 0;">
            <p style="font-size: 0.9em;">
                If you wish to unsubscribe from these emails, please click <a href="{unsubscribe_link}" style="color: #2980b9;">here</a>.
            </p>
        </div>
        """

    send_email(email, subject, plain_body, html_body)