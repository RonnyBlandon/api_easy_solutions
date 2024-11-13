import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from core.config import get_secret

def send_email(subject: str, recipient: str, html_content: str):
    message = MIMEMultipart()
    message["From"] = get_secret("SMTP_USERNAME")
    message["To"] = recipient
    message["Subject"] = subject
    smtp_server = get_secret("SMTP_SERVER")
    smtp_port = get_secret("SMTP_PORT")
    smtp_username = get_secret("SMTP_USERNAME")
    smtp_password = get_secret("SMTP_PASSWORD")

    message.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(smtp_username, recipient, message.as_string())
    except Exception as e:
        print(f"Error al enviar el correo: {e}")