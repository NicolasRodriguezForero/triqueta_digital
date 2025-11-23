"""
Application configuration using Pydantic Settings.
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings.
    All settings can be overridden by environment variables.
    """
    
    # Application
    APP_NAME: str = "Triqueta Digital API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    # Database
    DATABASE_URL: str
    DB_ECHO: bool = False
    
    # Redis
    REDIS_URL: str
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    
    # CORS - Simple string, split by comma
    BACKEND_CORS_ORIGINS: str = ""
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_LOGIN: str = "5/15minute"
    RATE_LIMIT_REGISTER: str = "3/hour"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
