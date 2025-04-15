from fastapi_mail import ConnectionConfig

from src.core.config import settings

mail_client = ConnectionConfig(
    MAIL_USERNAME=settings.mail.username,
    MAIL_PASSWORD=settings.mail.password,
    MAIL_FROM=settings.mail.from_email,
    MAIL_PORT=settings.mail.port,
    MAIL_SERVER=settings.mail.server,
    MAIL_FROM_NAME=settings.mail.from_name,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=False,
)
