import os
import json

from dotenv import load_dotenv

load_dotenv()


class Config:
    @staticmethod
    def load():
        """Loads configuration settings."""
        with open('config.json', 'r') as f:
            config = json.load(f)
        return config

    @staticmethod
    def get_env_variable(key, default=None):
        """Get environment variable or return default."""
        return os.getenv(key, default)
