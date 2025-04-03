from typing import Any, Dict, List, Optional, Union
from pydantic import AnyHttpUrl, PostgresDsn, RedisDsn, field_validator, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""
    
    # Project info
    PROJECT_NAME: str = "Tao Watch"
    PROJECT_DESCRIPTION: str = "Asynchronous API service for monitoring and interacting with the Bittensor blockchain"
    PROJECT_VERSION: str = "0.1.0"
    
    # API configuration
    API_V1_STR: str = "/api/v1"
    API_TOKEN: str = "test-api-token"
    
    # CORS configuration
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # PostgreSQL configuration
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "tao_watch"
    POSTGRES_PORT: str = "5432"
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    def assemble_db_connection(cls, v: Optional[str], info: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        
        values = info.data
        
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            port=int(values.get("POSTGRES_PORT", 5432)),
            path=f"{values.get('POSTGRES_DB') or ''}",
        )
    
    # Redis configuration
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    REDIS_URI: Optional[RedisDsn] = None
    
    @field_validator("REDIS_URI", mode="before")
    def assemble_redis_connection(cls, v: Optional[str], info: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
            
        values = info.data
        
        return RedisDsn.build(
            scheme="redis",
            username="",
            password=values.get("REDIS_PASSWORD", ""),
            host=values.get("REDIS_HOST", ""),
            port=values.get("REDIS_PORT", 6379),
            path=f"/{values.get('REDIS_DB', 0)}",
        )
    
    # Cache configuration
    CACHE_EXPIRATION_SECONDS: int = 120  # 2 minutes
    
    # Authentication
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Bittensor configuration - will be expanded in later PRs
    BITTENSOR_NETWORK: str = Field(
        default="test",
        description="Network to connect to ('finney' or 'test')"
    )
    BITTENSOR_WALLET_SEED: str = ""
    
    # Celery configuration
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"
    
    # Environment configuration
    ENVIRONMENT: str = "development"  # 'development', 'staging', 'production'
    DEBUG: bool = True
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # External APIs
    DATURA_API_KEY: str = ""
    CHUTES_API_KEY: str = ""
    
    # Bittensor Network Settings
    bittensor_finney_endpoint: str = Field(
        default="wss://entrypoint-finney.opentensor.ai:443",
        description="WebSocket endpoint for Bittensor Finney network"
    )
    bittensor_test_endpoint: str = Field(
        default="wss://test.finney.opentensor.ai:9944",
        description="WebSocket endpoint for Bittensor test network"
    )
    
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        extra="allow"  # Allow extra fields from environment variables
    )


settings = Settings() 