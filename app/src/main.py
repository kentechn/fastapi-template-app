import uvicorn
from fastapi import (
  FastAPI,
)

from src.api.endpoints import tasks

app = FastAPI()


app.include_router(tasks.router, tags=["Tasks"], prefix="/tasks")

if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8000)
