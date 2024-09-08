from sqlmodel import Field, SQLModel


class PostBase(SQLModel):
    title: str
    body: str


class Post(PostBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    userId: int = Field(index=True)


class PostCreate(PostBase):
    userId: int


class PostPublic(PostBase):
    id: int
    userId: int


class PostPatch(PostBase):
    title: str | None = None
    body: str | None = None
