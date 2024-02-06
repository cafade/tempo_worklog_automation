import enum
from logging import DEBUG, ERROR, INFO, WARNING

from pydantic_settings import BaseSettings, SettingsConfigDict


class LogLevel(enum.Enum):
    """Log levels."""

    DEBUG = DEBUG
    INFO = INFO
    WARNING = WARNING
    ERROR = ERROR


class Settings(BaseSettings):
    """Application settings."""

    # Current environment
    environment: str = "dev"

    # Testing
    run_integration_tests: bool = True

    log_level: LogLevel = LogLevel.INFO

    # API calls credentials and variables
    jira_account_email: str
    jira_token: str
    jira_base_api_url: str

    tempo_oauth_token: str
    author_account_id: str
    tempo_base_api_url: str

    model_config = SettingsConfigDict(
        env_prefix="TEMPO_WORKLOG_AUTOMATION_",
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()  # type: ignore
