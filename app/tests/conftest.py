from collections.abc import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from app.api.main import api_router
from app.core.config import settings
from app.models.post import Post  # noqa: F401

# TODO: figure out how to override db dependency on TestClient
app = FastAPI(title=f"{settings.PROJECT_NAME}_test")
app.include_router(api_router)


SQLALCHEMY_DB_URL = "sqlite://"
engine = create_engine(
    SQLALCHEMY_DB_URL,
    connect_args={"check_same_thread": False},
)


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        # db init here:
        SQLModel.metadata.create_all(engine)
        yield session
        # db cleanup here:


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client
