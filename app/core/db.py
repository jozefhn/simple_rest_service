from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine

# TODO: move into app config file
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
# sqlite_url = 'sqlite://'  # in memory disposable db

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/fastapi/full-stack-fastapi-template/issues/28


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_db_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
