from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
import os
from dotenv import load_dotenv
load_dotenv()


env_config = ConnectionConfig(
    MAIL_USERNAME = os.getenv("SEND_EMAIL"),
    MAIL_PASSWORD = os.getenv("SEND_EMAIL_PASSWORD"),
    MAIL_FROM = os.getenv("SEND_EMAIL"),
    MAIL_PORT = 587,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_FROM_NAME="Ntoju Email",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True,
    TEMPLATE_FOLDER='templates'
)