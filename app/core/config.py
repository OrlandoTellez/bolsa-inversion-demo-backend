import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""
    
    # App
    APP_NAME: str = "Bolsa de Inversiones Nicaragua API"
    DEBUG: bool = True
    
    # JWT
    SECRET_KEY: str = "bolsa-inversion-demo-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:5050",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5050",
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
