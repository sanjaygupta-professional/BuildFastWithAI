"""Configuration management for TweetInsight application."""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    # Application
    APP_NAME: str = "TweetInsight"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = Field(default=False, description="Enable debug mode")

    # Twitter API
    TWITTER_API_KEY: Optional[str] = Field(default=None, description="Twitter API Key")
    TWITTER_API_SECRET: Optional[str] = Field(default=None, description="Twitter API Secret")
    TWITTER_ACCESS_TOKEN: Optional[str] = Field(default=None, description="Twitter Access Token")
    TWITTER_ACCESS_SECRET: Optional[str] = Field(default=None, description="Twitter Access Token Secret")
    TWITTER_BEARER_TOKEN: Optional[str] = Field(default=None, description="Twitter Bearer Token")

    # LLM API (supports both OpenAI and Anthropic)
    LLM_PROVIDER: str = Field(default="openai", description="LLM provider: openai or anthropic")
    OPENAI_API_KEY: Optional[str] = Field(default=None, description="OpenAI API Key")
    ANTHROPIC_API_KEY: Optional[str] = Field(default=None, description="Anthropic API Key")
    LLM_MODEL: str = Field(default="gpt-4-turbo-preview", description="LLM model name")
    EMBEDDING_MODEL: str = Field(default="text-embedding-3-small", description="Embedding model")

    # Database
    DATABASE_PATH: str = Field(default="./data/tweetinsight.db", description="SQLite database path")
    VECTOR_DB_PATH: str = Field(default="./data/chromadb", description="ChromaDB storage path")

    # Application Limits
    MAX_HANDLES_PER_COLLECTION: int = Field(default=5, description="Max Twitter handles per collection")
    MAX_TWEETS_PER_HANDLE: int = Field(default=200, description="Max tweets to fetch per handle")
    MAX_COLLECTIONS_FREE: int = Field(default=3, description="Max collections for free tier")
    MAX_QUERIES_FREE: int = Field(default=100, description="Max queries per month for free tier")

    # Performance
    REQUEST_TIMEOUT: int = Field(default=30, description="API request timeout in seconds")
    CHUNK_SIZE: int = Field(default=1000, description="Chunk size for text processing")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings."""
    return settings
