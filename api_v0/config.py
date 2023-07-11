import os
from pydantic import BaseSettings
from functools import lru_cache
from dotenv import load_dotenv
import openai


load_dotenv()
openai.api_key = os.getenv("openai_key")

class Settings(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 5000

 
@lru_cache()
def get_settings() -> Settings:
    return Settings()

    