from typing import Any

from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exception_handlers import (
  http_exception_handler,
  request_validation_exception_handler,
)
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse


class ApiException(Exception):
  def __init__(self, name: str) -> None:
    self.name = name


async def custom_http_exception_handler(
  request: Request, exc: HTTPException
) -> JSONResponse:  # noqa: ANN401
  print(f"OMG! An HTTP error!: {repr(exc)}")
  return await http_exception_handler(request, exc)


async def custom_validation_exception_handler(
  request: Request, exc: RequestValidationError
) -> JSONResponse:
  print(f"OMG! An validation error!: {repr(exc)}")
  return await request_validation_exception_handler(request, exc)
