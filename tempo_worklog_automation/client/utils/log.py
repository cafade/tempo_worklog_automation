#!/usr/bin/python3

import logging
import sys
from typing import Dict


class DispatchingFormatter:
    def __init__(
        self,
        formatters: Dict[str, logging.Formatter],
        default_formatter: logging.Formatter,
    ):
        self._formatters = formatters
        self._default_formatter = default_formatter

    def format(self, record: logging.LogRecord) -> str:
        formatter = self._formatters.get(record.levelname, self._default_formatter)
        return formatter.format(record)


class LoggingClass:
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
        self.new_logger = logging.getLogger(self.name)
        self.new_logger.setLevel(self.level)
        self.new_logger.addHandler(self.handler)
        new_handler = self.handler
        new_handler.setFormatter(self.logger_formats)  # type: ignore
        self.new_logger.addHandler(new_handler)
        return self.new_logger


if __name__ == "__main__":
    pass
