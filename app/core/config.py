import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""
    
    # App
    APP_NAME: str = "Bolsa de Inversiones Nicaragua API"
    DEBUG: bool = False
    
    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # CORS
    CORS_ORIGINS: list[str] = []
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
