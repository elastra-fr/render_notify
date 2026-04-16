import smtplib
from email.mime.text import MIMEText
from .keyring_store import get_email_credentials


def send_email_notification(subject, message, smtp_host="smtp.gmail.com", smtp_port=465):
    email, password = get_email_credentials()
    if not email or not password:
        print("[RenderNotify] Email credentials not found. Set them in addon preferences.")
        return

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = email
    msg["To"] = email

    try:
        with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
            server.login(email, password)
            server.send_message(msg)
        print("[RenderNotify] Email sent successfully.")
    except Exception as e:
        print(f"[RenderNotify] Failed to send email: {e}")