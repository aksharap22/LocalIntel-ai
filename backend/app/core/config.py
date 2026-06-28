from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "LocalIntel AI"
    environment: str = "offline"
    database_url: str = "sqlite:///./localintel.db"
    upload_dir: Path = Path("outputs/uploads")
    export_dir: Path = Path("outputs/exports")
    llama_cpp_binary: str = "llama-cli"
    llama_model_path: Path = Path("models/llm/model.gguf")
    whisper_cpp_binary: str = "whisper-cli"
    whisper_model_path: Path = Path("models/whisper/ggml-base.en.bin")
    max_upload_mb: int = 100
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    model_config = SettingsConfigDict(env_file=".env", env_prefix="LOCALINTEL_")

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.upload_dir.mkdir(parents=True, exist_ok=True)
    settings.export_dir.mkdir(parents=True, exist_ok=True)
    return settings
