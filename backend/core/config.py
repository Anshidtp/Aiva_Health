from functools import lru_cache
from typing import List
 
from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
 
 
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
 
    # ── Application ──────────────────────────────────────────────────────────
    app_env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    app_reload: bool = True
    secret_key: str = "change-me"
    access_token_expire_minutes: int = 60
 
    # ── Database ─────────────────────────────────────────────────────────────
    db_host: str = "localhost"
    db_port: int = 1433
    db_name: str = "DentalDB"
    db_user: str = "sa"
    db_password: str = ""
    db_driver: str = "ODBC Driver 18 for SQL Server"
    db_echo: bool = False
    db_pool_size: int = 10
    db_max_overflow: int = 20
 
    # ── AI / LLM ─────────────────────────────────────────────────────────────
    groq_api_key: str = ""
    groq_model: str = "llama3-70b-8192"
    groq_temperature: float = 0.0
    groq_max_tokens: int = 1024
    langgraph_recursion_limit: int = 25
 
    # ── Voice ─────────────────────────────────────────────────────────────────
    whisper_model: str = "base"
    whisper_device: str = "cpu"
    tts_provider: str = "gtts"
    elevenlabs_api_key: str = ""
    elevenlabs_voice_id: str = "21m00Tcm4TlvDq8ikWAM"
 
    # ── Rate Limiting ─────────────────────────────────────────────────────────
    rate_limit_per_minute: int = 60
 
    # ── CORS ──────────────────────────────────────────────────────────────────
    allowed_origins: str = "http://localhost:3000"
 
    # ── Computed ──────────────────────────────────────────────────────────────
    @computed_field  # type: ignore[prop-decorator]
    @property
    def database_url(self) -> str:
        """Sync SQLAlchemy connection string for MSSQL via pyodbc."""
        driver = self.db_driver.replace(" ", "+")
        return (
            f"mssql+pyodbc://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
            f"?driver={driver}&TrustServerCertificate=yes"
        )
 
    @computed_field  # type: ignore[prop-decorator]
    @property
    def async_database_url(self) -> str:
        """Async SQLAlchemy connection string (aioodbc)."""
        driver = self.db_driver.replace(" ", "+")
        return (
            f"mssql+aioodbc://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
            f"?driver={driver}&TrustServerCertificate=yes"
        )
 
    @computed_field  # type: ignore[prop-decorator]
    @property
    def cors_origins(self) -> List[str]:
        return [o.strip() for o in self.allowed_origins.split(",")]
 
    @property
    def is_production(self) -> bool:
        return self.app_env == "production"
 
 
@lru_cache
def get_settings() -> Settings:
    """Cached singleton — call get_settings() anywhere."""
    return Settings()
 
 
# Module-level alias for convenience
settings: Settings = get_settings()