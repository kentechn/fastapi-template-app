import logging
import os
from logging.config import dictConfig


def _get_log_level() -> int:
  """
  DEBUG環境変数に基づいてログレベルを取得します

  Returns:
    int: ロギングに使用するログレベル

  """
  debug_env = os.getenv("DEBUG", "False").lower()
  if debug_env in ["1", "true", "yes"]:
    return logging.DEBUG
  else:
    return logging.WARNING


def setup_logging() -> None:
  log_level = _get_log_level()

  logging_config = {
    "version": 1,
    "formatters": {
      "default": {
        "format": "[%(levelname)s] %(asctime)s [%(processName)s: %(process)d] "
        "[%(threadName)s: %(thread)d] "
        "%(name)s:%(lineno)d %(funcName)s: %(message)s",
      },
      "uvicorn": {
        "()": "uvicorn.logging.DefaultFormatter",
        "format": "%(levelprefix)s %(asctime)s - %(message)s",
        "datefmt": "%Y-%m-%d %H:%M:%S",
      },
    },
    "handlers": {
      "default": {
        "class": "logging.StreamHandler",
        "formatter": "default",
        "stream": "ext://sys.stderr",
      },
      "uvicorn.access": {
        "class": "logging.StreamHandler",
        "formatter": "uvicorn",
      },
    },
    "loggers": {
      "": {
        "handlers": ["default"],
        "level": log_level,
        "propagate": False,
      },
      "uvicorn.error": {
        "handlers": ["default"],
        "level": log_level,
        "propagate": False,
      },
      "uvicorn.access": {
        "handlers": ["uvicorn.access"],
        "level": "INFO",
        "propagate": False,
      },
    },
  }

  dictConfig(logging_config)
