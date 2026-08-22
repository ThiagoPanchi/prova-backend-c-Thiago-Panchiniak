from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Drone Mapping API"
    app_env: str = "development"
    debug: bool = False
    api_prefix: str = "/api/v1"
    database_url: str = "sqlite:///./missions.db"
    redis_url: str = "redis://localhost:6379/0"
    secret_key: str = "change-this-secret-key"
    access_token_expire_minutes: int = 30
    ai_model_name: str = "aerial_mapping_yolo"
    ai_model_version: str = "1.0.0"
    max_image_size_mb: int = 50

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
