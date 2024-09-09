from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.main import api_router
from app.core.config import settings
from app.core.db import create_db_and_tables, engine


# TODO: use alembic migrations
@asynccontextmanager
async def lifespan(_: FastAPI):
    # on startup do this:
    create_db_and_tables(engine)
    yield
    # on shutdown do this:


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

app.include_router(api_router)
