from pydantic_settings import BaseSettings
from pydantic import model_validator
from typing import Optional


class CloudConfig(BaseSettings):
    # AWS_ACCESS_KEY_ID: str = ""
    AWS_TE_ACCESS_KEY_ID: str = ""
    # AWS_SECRET_ACCESS_KEY: str = ""
    AWS_TE_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = ""
    S3_BUCKET_NAME: str = ""


class QueueConfig(BaseSettings):
    RABBITMQ_USER: str = ""
    RABBITMQ_PASSWORD: str = ""
    RABBITMQ_HOST: str = ""
    RABBITMQ_PORT: int = 5672
    QUEUE_NAME: str = ""


class DBConfig(BaseSettings):
    POSTGRES_HOST: str = ""
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""
    POSTGRES_SCHEMA: str = "public"


class LLMConfig(BaseSettings):
    LLM_PROVIDER: str = "gemini"  # gemini | openai
    USE_MOCK_LLM: bool = True

    GEMINI_API_KEY: str | None = None
    OPENAI_API_KEY: str | None = None


class Settings(BaseSettings):
    APP_NAME: str = "DocQuery Application"
    APP_PORT: int = 8000
    ENV: str = "dev"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    CLOUD_CONFIG: Optional[CloudConfig] = None
    QUEUE_CONFIG: Optional[QueueConfig] = None
    DB_CONFIG: Optional[DBConfig] = None
    LLM_CONFIG: Optional[LLMConfig] = None

    @model_validator(mode="after")
    def build_nested_configs(self):
        if self.CLOUD_CONFIG is None:
            self.CLOUD_CONFIG = CloudConfig()
        if self.QUEUE_CONFIG is None:
            self.QUEUE_CONFIG = QueueConfig()
        if self.DB_CONFIG is None:
            self.DB_CONFIG = DBConfig()
        if self.LLM_CONFIG is None:
            self.LLM_CONFIG = LLMConfig()
        return self

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
