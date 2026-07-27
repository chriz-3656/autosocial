import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # AI Providers
    groq_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    
    # Instagram Credentials
    instagram_username: Optional[str] = None
    instagram_password: Optional[str] = None
    
    # Render & Environment Defaults
    playwright_browser_path: Optional[str] = None
    timezone: str = "UTC"
    default_language: str = "en"
    default_brand: str = "autosocial"
    
    # System
    log_level: str = "INFO"
    database_url: str = "sqlite:///./autosocial.db"
    redis_url: Optional[str] = None
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
