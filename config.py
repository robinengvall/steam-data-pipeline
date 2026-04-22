"""
Configuration management for Steam Data Pipeline.
Loads and validates environment variables at startup.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration loaded from environment variables."""
    
    # Steam API Configuration
    STEAM_API_KEY = os.getenv("STEAM_API_KEY")
    STEAM_ID = os.getenv("STEAM_ID")
    STEAM_API_BASE_URL = "https://api.steampowered.com"
    
    # MongoDB Configuration
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "steam_data")
    
    # Collections
    SNAPSHOTS_COLLECTION = "game_snapshots"
    
    @classmethod
    def validate(cls):
        """Validate that required configuration values are present."""
        missing = []
        
        if not cls.STEAM_API_KEY:
            missing.append("STEAM_API_KEY")
        if not cls.STEAM_ID:
            missing.append("STEAM_ID")
            
        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}\n"
                f"Please check your .env file."
            )
        
        return True


# Validate configuration on import
Config.validate()
