from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application
    app_name: str = "eDocs AI"
    app_version: str = "0.1.0"
    environment: str = "development"
    debug: bool = True

    # API
    api_prefix: str = "/api/v1"

    # Database
    database_url: str = (
        "postgresql+psycopg://edocs_ai:edocs_ai@localhost:5432/edocs_ai"
    )

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # eDocs
    edocs_base_url: str = "http://localhost"
    edocs_api_key: str = ""

    # AI / LLM
    llm_provider: str = "ollama"
    llm_base_url: str = "http://localhost:11434"
    llm_model: str = "qwen3:8b"

    # Embeddings
    embedding_model: str = "BAAI/bge-small-en-v1.5"

    # OCR
    ocr_enabled: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()