"""
Configuration settings for the Oil & Gas Financial Analysis Chatbot
"""

import os
from pathlib import Path

class Config:
    """Configuration class for the chatbot."""
    
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    
    # Database settings
    DATABASE_PATH = "data/financial_chatbot.db"
    
    # Data directory
    DATA_DIR = Path("data")
    
    # Companies to track
    TRACKED_COMPANIES = [
        "Shell",
        "BP", 
        "ExxonMobil",
        "Chevron"
    ]
    
    # OpenAI settings
    OPENAI_MODEL = "gpt-4o"  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024
    OPENAI_MAX_TOKENS = 2000
    OPENAI_TEMPERATURE = 0.3  # Lower temperature for more consistent financial analysis
    
    # Logging settings
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    @classmethod
    def ensure_directories(cls):
        """Ensure required directories exist."""
        cls.DATA_DIR.mkdir(exist_ok=True)
