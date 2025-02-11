import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", ".env.prod"),
        extra="ignore",
    )
    # DB
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    # AUTH
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = Field(..., env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(120, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    # PINECONE
    PINECONE_API_KEY: str = Field(..., env="PINECONE_API_KEY")
    PINECONE_INDEX_NAME: str = Field(..., env="PINECONE_INDEX_NAME")

    # OPENAI
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    OPENAI_MODEL_NAME: str = Field(..., env="OPENAI_MODEL_NAME")
    OPENAI_TEMPERATURE: float = Field(0.1, env="OPENAI_TEMPERATURE")
    OPENAI_MAX_TOKENS: int = Field(4096, env="OPENAI_MAX_TOKENS")
    EMBEDDING_MODEL_NAME: str = Field(..., env="EMBEDDING_MODEL_NAME")

    # prompt
    OPENAI_SYSTEM_PROMPT: str = Field(..., env="OPENAI_SYSTEM_PROMPT")
    OPENAI_USER_PROMPT: str = Field(..., env="OPENAI_USER_PROMPT")

settings = Settings()