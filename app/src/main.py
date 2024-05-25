from typing import Any

import uvicorn
from fastapi import (
  FastAPI,
  Request,
)
from fastapi.exceptions import HTTPException, RequestValidationError

from src.api.endpoints import tasks
from src.extensions.exception_handlers import (
  custom_http_exception_handler,
  custom_validation_exception_handler,
)

app = FastAPI()

app.add_exception_handler(RequestValidationError, custom_validation_exception_handler)
app.add_exception_handler(HTTPException, custom_http_exception_handler)


app.include_router(tasks.router, tags=["Tasks"], prefix="/tasks")

if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8000)
