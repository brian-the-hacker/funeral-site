import os
from dotenv import load_dotenv

load_dotenv()


def _list(v: str) -> list[str]:
    return [x.strip() for x in v.split(",") if x.strip()]


class Settings:
    cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME", "")
    api_key = os.getenv("CLOUDINARY_API_KEY", "")
    api_secret = os.getenv("CLOUDINARY_API_SECRET", "")
    folder = os.getenv("CLOUDINARY_FOLDER", "makueni-pamoja")
    admin_user = os.getenv("ADMIN_USERNAME", "admin")
    admin_password = os.getenv("ADMIN_PASSWORD", "")
    jwt_secret = os.getenv("JWT_SECRET", "")
    database_url = os.getenv("DATABASE_URL", "sqlite:///./site.db")
    cors_origins = _list(os.getenv("CORS_ORIGINS", "http://localhost:5500"))
    smtp_host = os.getenv("SMTP_HOST", "")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER", "")
    smtp_password = os.getenv("SMTP_PASSWORD", "")
    notify_to = os.getenv("NOTIFY_TO", "")


settings = Settings()
