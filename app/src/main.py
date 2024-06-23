import logging
import sys
from typing import Any

import uvicorn
from debug_toolbar.middleware import DebugToolbarMiddleware
from fastapi import Depends, FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError

from src.api.endpoints import tasks
from src.config import Settings, get_settings
from src.extensions.exception_handlers import (
  custom_http_exception_handler,
  custom_validation_exception_handler,
)
from src.logger import setup_logging

setup_logging()

logger = logging.getLogger(__name__)

app = FastAPI(debug=True)
app.add_middleware(
  DebugToolbarMiddleware,
  panels=["debug_toolbar.panels.sqlalchemy.SQLAlchemyPanel"],
)


app.add_exception_handler(RequestValidationError, custom_validation_exception_handler)
app.add_exception_handler(HTTPException, custom_http_exception_handler)

app.include_router(tasks.router, tags=["Tasks"], prefix="/tasks")


@app.get("/ping")
async def pong(settings: Settings = Depends(get_settings)):
  logger.debug("Pinging the server")
  return {
    "ping": "pong!",
    "environment": "dev",
    "testing": True,
  }


if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8000)
