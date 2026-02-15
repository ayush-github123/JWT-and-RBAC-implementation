import logging
import sys
from logging.config import dictConfig
from typing import Optional


def setup_logging(level: Optional[str] = "INFO") -> None:
    """
    Configure application-wide logging.
    Supports structured logging and can be extended
    for JSON logs in production.
    """

    log_level = level.upper()

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,

            "formatters": {
                "default": {
                    "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                },
                "detailed": {
                    "format": "%(asctime)s | %(levelname)s | %(name)s | %(filename)s:%(lineno)d | %(message)s",
                },
            },

            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "stream": sys.stdout,
                    "formatter": "default",
                },
            },

            "loggers": {
                "": {  # root logger
                    "handlers": ["console"],
                    "level": log_level,
                },
                "uvicorn": {
                    "handlers": ["console"],
                    "level": log_level,
                    "propagate": False,
                },
                "uvicorn.error": {
                    "level": log_level,
                },
                "uvicorn.access": {
                    "level": log_level,
                },
            },
        }
    )
