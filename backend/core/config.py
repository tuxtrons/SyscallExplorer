"""
Configuration settings for SystemCallExplorer backend
"""

import os
from typing import List
from pydantic import BaseSettings

class Settings(BaseSettings):
    """Application settings"""
    
    # Server configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # CORS settings
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]
    
    # Database settings (for future use)
    DATABASE_URL: str = "sqlite:///./systemcalls.db"
    
    # System call analysis settings
    MAX_TRACE_DURATION: int = 300  # Maximum trace duration in seconds
    MAX_TRACE_PROCESSES: int = 100  # Maximum number of processes to trace
    
    # Performance settings
    CACHE_TIMEOUT: int = 3600  # Cache timeout in seconds
    MAX_CONCURRENT_ANALYSES: int = 10
    
    # Security settings
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # File paths
    TEMP_DIR: str = "/tmp/systemcall_explorer"
    LOG_DIR: str = "./logs"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Global settings instance
settings = Settings()