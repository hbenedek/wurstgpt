import os
import smtplib
from email.mime.text import MIMEText


def send_email(user, pwd, recipient, subject, body):
    msg = MIMEText(body)
    msg["From"] = os.environ.get("EMAIL")
    msg["To"] = os.environ.get("EMAIL")
    msg["Subject"] = "WurstGPT"

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(user, pwd)
        server.send_message(msg)
