from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    MONGO_URL: str = os.getenv("MONGO_URL", "mongodb://localhost:27017")
    DB_NAME: str = os.getenv("DB_NAME", "lms_db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "fallback_secret_key")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "uploads/")

    class Config:
        env_file = ".env"

settings = Settings()
