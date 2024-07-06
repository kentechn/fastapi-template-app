# structlogの設定
import logging
import os
from logging.config import dictConfig
from typing import Any

import structlog

log_level = os.environ.get("LOG_LEVEL", "DEBUG").upper()


logging.basicConfig(format="%(message)s", level=log_level)


common_processors = [
  structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M.%S", utc=False),
  structlog.stdlib.add_log_level,
  structlog.stdlib.PositionalArgumentsFormatter(),
]


def extract_from_record(_: Any, __: Any, event_dict: dict) -> dict:
  """
  Extract thread and process names and add them to the event dict.
  """
  record = event_dict["_record"]
  event_dict["thread_name"] = record.thread
  event_dict["process_name"] = record.process
  return event_dict


log_config = {
  "version": 1,
  "disable_existing_loggers": False,
  "formatters": {
    "json": {
      "()": structlog.stdlib.ProcessorFormatter,
      "processors": [
        extract_from_record,
        structlog.stdlib.ProcessorFormatter.remove_processors_meta,
        structlog.processors.JSONRenderer(),
      ],
      "foreign_pre_chain": common_processors,
    },
    "colored": {
      "()": structlog.stdlib.ProcessorFormatter,
      "processors": [
        extract_from_record,
        structlog.stdlib.ProcessorFormatter.remove_processors_meta,
        structlog.processors.JSONRenderer(),
      ],
      "foreign_pre_chain": common_processors,
    },
  },
  "handlers": {
    "default": {
      "class": "logging.StreamHandler",
      "formatter": "colored",
    },
    "file": {
      "class": "logging.handlers.WatchedFileHandler",
      "filename": "test.log",
      "formatter": "json",
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
      "level": "INFO",
      "propagate": False,
    },
    "uvicorn.access": {
      "handlers": ["default"],
      "level": "INFO",
      "propagate": False,
    },
  },
}

dictConfig(log_config)


processors = common_processors + [
  structlog.processors.CallsiteParameterAdder(
    [
      structlog.processors.CallsiteParameter.FILENAME,
      structlog.processors.CallsiteParameter.FUNC_NAME,
      structlog.processors.CallsiteParameter.LINENO,
    ]
  ),
  structlog.processors.dict_tracebacks,
  structlog.processors.StackInfoRenderer(),
  structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
]

structlog.configure(
  processors=processors,
  context_class=dict,
  logger_factory=structlog.stdlib.LoggerFactory(),
  cache_logger_on_first_use=True,
)


# ログインスタンスの作成
logger = structlog.get_logger()
