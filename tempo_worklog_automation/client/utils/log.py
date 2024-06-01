import logging
import sys
from typing import Dict


class DispatchingFormatter:
    """Settings object for logging class."""

    def __init__(
        self,
        formatters: Dict[str, logging.Formatter],
        default_formatter: logging.Formatter,
    ):
        self._formatters = formatters
        self._default_formatter = default_formatter

    def format(self, record: logging.LogRecord) -> str:
        """
        Get log record and set format for it.

        :param record: record to format.
        :return: string of formatted log record.
        """
        formatter = self._formatters.get(record.levelname, self._default_formatter)
        return formatter.format(record)


class LoggingClass:
    """
    Create logging.Logger and set format and log levels.

    :param name: Logger name.
    :param level: default Logger name.
    :param handler: Logger Handler class.
    """

    def __init__(
        self,
        name: str = __name__,
        level: int = logging.INFO,
        handler: logging.Handler = logging.StreamHandler(sys.stdout),
    ):
        self.logger_formats = DispatchingFormatter(
            formatters={
                "ERROR": logging.Formatter(
                    "%(levelname)s[%(asctime)s] - %(threadName)s -"
                    " %(filename)s:%(lineno)s - %(funcName)s() -- %(message)s",
                ),
                "DEBUG": logging.Formatter(
                    "%(levelname)s[%(asctime)s] - %(threadName)s -"
                    " %(filename)s:%(lineno)s - %(funcName)s() -- %(message)s",
                ),
                "INFO": logging.Formatter("%(asctime)s -- %(message)s"),
            },
            default_formatter=logging.Formatter("%(message)s"),
        )

        self.name = name
        self.level = level
        self.new_logger: logging.Logger
        self.level = level
        self.handler = handler

    def create_logger(self) -> logging.Logger:
        """
        Instantiate Logger and return it.

        :return: logging.Logger object.
        """
        self.new_logger = logging.getLogger(self.name)
        self.new_logger.setLevel(self.level)
        self.new_logger.addHandler(self.handler)
        new_handler = self.handler
        new_handler.setFormatter(self.logger_formats)  # type: ignore
        self.new_logger.addHandler(new_handler)
        return self.new_logger
