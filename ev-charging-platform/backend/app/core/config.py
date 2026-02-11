from pydantic_settings import BaseSettings
from typing import List
import os
from pathlib import Path

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "EV Charging Platform"
    DEBUG: bool = True
    VERSION: str = "1.0.0"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8081",
        "http://localhost:19006",  # Expo
        "exp://localhost:19000",   # Expo Go
    ]
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/evcharging"
    DB_ECHO: bool = False
    
    # Firebase
    FIREBASE_CREDENTIALS_PATH: str = "firebase-credentials.json"
    FIREBASE_DATABASE_URL: str = ""
    
    # Stripe
    STRIPE_SECRET_KEY: str = ""
    STRIPE_PUBLISHABLE_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""
    
    # Google Maps
    GOOGLE_MAPS_API_KEY: str = ""
    
    # Charging Provider APIs
    CHARGEPOINT_API_KEY: str = ""
    CHARGEPOINT_API_URL: str = "https://api.chargepoint.com/v1"
    
    EVGO_API_KEY: str = ""
    EVGO_API_URL: str = "https://api.evgo.com/v1"
    
    ELECTRIFY_AMERICA_API_KEY: str = ""
    ELECTRIFY_AMERICA_API_URL: str = "https://api.electrifyamerica.com/v1"
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = ""
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    # Session defaults
    DEFAULT_SESSION_TIMEOUT_MINUTES: int = 240  # 4 hours
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
