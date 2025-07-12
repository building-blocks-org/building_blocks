from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from examples.tasker_primitives.src.presentation.http.routes.task_routes import (
    router as task_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print("🚀 Starting Tasker Primitives Example")
    yield
    print("🛑 Shutting down Tasker Primitives Example")


app = FastAPI(
    title="Tasker Primitives Example",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(task_router)
