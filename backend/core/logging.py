import logging
import os
from logging.config import dictConfig
from logging.handlers import RotatingFileHandler
from typing import Optional


LOG_DIR = "logs"
LOG_FILE = "app.log"


def setup_logging(level: Optional[str] = "INFO") -> None:
    """
    Configure application-wide logging.
    Logs to both console and file with rotation support.
    """

    os.makedirs(LOG_DIR, exist_ok=True)
    log_path = os.path.join(LOG_DIR, LOG_FILE)

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
                    "formatter": "default",
                },
                "file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": log_path,
                    "maxBytes": 5 * 1024 * 1024,  # 5MB
                    "backupCount": 5,
                    "formatter": "detailed",
                    "encoding": "utf-8",
                },
            },

            "loggers": {
                "": {
                    "handlers": ["console", "file"],
                    "level": log_level,
                },
                "uvicorn": {
                    "handlers": ["console", "file"],
                    "level": log_level,
                    "propagate": False,
                },
                "uvicorn.error": {
                    "handlers": ["console", "file"],
                    "level": log_level,
                    "propagate": False,
                },
                "uvicorn.access": {
                    "handlers": ["console", "file"],
                    "level": log_level,
                    "propagate": False,
                },
            },
        }
    )
