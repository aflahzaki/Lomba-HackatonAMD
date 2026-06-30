"""Application configuration using Pydantic settings."""

import os
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Fireworks AI
    FIREWORKS_API_KEY: str = ""
    FIREWORKS_MODEL: str = "accounts/fireworks/models/llama-v3p1-8b-instruct"
    FIREWORKS_API_URL: str = "https://api.fireworks.ai/inference/v1/chat/completions"

    # Model paths
    MODEL_PATH: str = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "models",
        "prediction_model.joblib",
    )

    # SIDATA SQL path - works both in-container (/database/seed_sidata.sql)
    # and on host (relative to project root)
    SIDATA_SQL_PATH: str = (
        "/database/seed_sidata.sql"
        if os.path.exists("/database/seed_sidata.sql")
        else os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "database",
            "seed_sidata.sql",
        )
    )

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # CORS
    CORS_ORIGINS: List[str] = ["*"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
