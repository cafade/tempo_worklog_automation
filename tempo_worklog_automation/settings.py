import enum
from logging import DEBUG, ERROR, INFO, WARNING

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class LogLevel(enum.Enum):
    """Log levels."""

    DEBUG = DEBUG
    INFO = INFO
    WARNING = WARNING
    ERROR = ERROR


class Settings(BaseSettings):
    """Application settings."""

    @field_validator("log_level", mode="before")
    def validate_log_level(cls, value: str) -> LogLevel:  # noqa: N805
        """
        Validate that the log level is a valid LogLevel enum member.

        :param value: validation string.
        :raises ValueError: when field_validator condition fails.
        :return: enum log level.
        """
        try:
            return LogLevel[value.upper()]
        except KeyError:
            raise ValueError(
                "Invalid log level, values values are: DEBUG, INFO, WARNING, and ERROR.",  # noqa: E501
            )

    log_level: LogLevel = LogLevel.INFO
    logger_name: str = "main_logger"

    # Current environment
    environment: str = "dev"

    # Testing
    run_integration_tests: bool = True

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
