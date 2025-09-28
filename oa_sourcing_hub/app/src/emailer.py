
import os, smtplib
from email.mime.text import MIMEText

def _smtp():
    host = os.getenv("EMAIL_SMTP_HOST","")
    port = int(os.getenv("EMAIL_SMTP_PORT","587"))
    user = os.getenv("EMAIL_USERNAME","")
    pwd  = os.getenv("EMAIL_PASSWORD","")
    return host, port, user, pwd

def send_mail(subject: str, body: str):
    if os.getenv("EMAIL_ENABLED","false").lower() != "true":
        return
    host, port, user, pwd = _smtp()
    from_addr = os.getenv("EMAIL_FROM", user)
    to_addr = os.getenv("EMAIL_TO","")
    if not (host and to_addr):
        return
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to_addr
    with smtplib.SMTP(host, port, timeout=20) as s:
        s.starttls()
        if user and pwd:
            s.login(user, pwd)
        s.sendmail(from_addr, [to_addr], msg.as_string())
