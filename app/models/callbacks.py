from sqlmodel import SQLModel


class ExternalUser(SQLModel):
    id: int


class ExternalPost(SQLModel):
    id: int
    userId: int
    title: str
    body: str
