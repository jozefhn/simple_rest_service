from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.main import api_router
from app.core.db import create_db_and_tables


# TODO: use alembic migrations
@asynccontextmanager
async def lifespan(_: FastAPI):
    # on startup do this:
    create_db_and_tables()
    yield
    # on shutdown do this:


# TODO: move vars into app config file
app = FastAPI(title="Simple REST service", lifespan=lifespan)

app.include_router(api_router)
