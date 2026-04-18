import smtplib
from email.mime.text import MIMEText
from .keyring_store import get_email_credentials


def send_email_notification(subject, message, smtp_host="smtp.gmail.com", smtp_port=465, use_tls=False, cc=""):
    email, password = get_email_credentials()
    if not email or not password:
        print("[RenderNotify] Email credentials not found. Set them in addon preferences.")
        return

    cc_list = [a.strip() for a in cc.split(",") if a.strip()] if cc else []
    recipients = [email] + cc_list

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = email
    msg["To"] = email
    if cc_list:
        msg["Cc"] = ", ".join(cc_list)

    try:
        if use_tls:
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.starttls()
                server.login(email, password)
                server.sendmail(email, recipients, msg.as_string())
        else:
            with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
                server.login(email, password)
                server.sendmail(email, recipients, msg.as_string())
        print("[RenderNotify] Email sent successfully.")
    except Exception as e:
        print(f"[RenderNotify] Failed to send email: {e}")