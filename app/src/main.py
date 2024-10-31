import logging
from typing import Any

import uvicorn
from debug_toolbar.middleware import DebugToolbarMiddleware
from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException, RequestValidationError

from src.api.endpoints import tasks
from src.core.config import settings
from src.core.logger import setup_logging
from src.extensions.exception_handlers import (
  custom_http_exception_handler,
  custom_validation_exception_handler,
)

setup_logging()

logger = logging.getLogger(__name__)

app = FastAPI(debug=True, root_path=settings.app_root_path)

app.add_middleware(
  DebugToolbarMiddleware,
  panels=["debug_toolbar.panels.sqlalchemy.SQLAlchemyPanel"],
)


@app.middleware("http")
async def logging_middleware(request: Request, call_next: Any) -> Any:
  # リクエスト情報をログに記録
  logger.warning(
    "request_started",
    method=request.method,
    url=str(request.url),
    client_ip=request.client.host,
  )

  response = await call_next(request)

  # レスポンス情報をログに記録
  await logger.ainfo("request_finished", status_code=response.status_code)

  return response


app.add_exception_handler(RequestValidationError, custom_validation_exception_handler)
app.add_exception_handler(HTTPException, custom_http_exception_handler)

app.include_router(tasks.router, tags=["Tasks"], prefix="/tasks")


@app.get("/")
async def pong() -> dict[str, Any]:
  await logger.warning("Pinging the server")

  try:
    raise ValueError("test error")
  except Exception as e:
    logger.exception(e)

  return {
    "msg": "I am task app api!",
  }


if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8000)
