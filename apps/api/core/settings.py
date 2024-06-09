from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    app_dir: str = str(Path.cwd())
    api_media_path: str
    api_media_url: str
    model_config = SettingsConfigDict()
    celery_broker_url: str
    celery_result_backend: str
    api_base_url: str


@lru_cache()
def get_settings():
    return Settings()
