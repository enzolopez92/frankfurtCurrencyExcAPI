import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration."""
    API_BASE_URL = os.getenv("FOREX_API_URL", "http://localhost:8080/v1")
    DEFAULT_BASE_CURRENCY = os.getenv("DEFAULT_BASE_CURRENCY", "EUR")
    REQUEST_TIMEOUT = 10
    CACHE_EXPIRY = 300  # 5 minutes
