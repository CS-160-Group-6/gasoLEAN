from pydantic import Field
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    # Database configuration
    DB_URL: str = Field('sqlite:///./data.db', env='DB_URL')
    os.environ['USE_EMULATOR'] = 'true'
    USE_EMULATOR: str = os.getenv(key='USE_EMULATOR').lower()

settings = Settings()