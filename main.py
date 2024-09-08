from contextlib import asynccontextmanager

import httpx
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select


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


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
# sqlite_url = 'sqlite://'  # in memory disposable db

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

external_api_url = "https://jsonplaceholder.typicode.com/"
external_users_url = f"{external_api_url}users/"
external_posts_url = f"{external_api_url}posts/"


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


@asynccontextmanager
async def lifespan(_: FastAPI):
    # on startup do this:
    create_db_and_tables()
    yield
    # on shutdown do this:


async def external_api_get(url):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            return response

        except httpx.RequestError as exc:
            # network error
            raise HTTPException(
                status_code=400, detail=f"Error response from external API: {exc}"
            )
        except httpx.HTTPStatusError as exc:
            # 4xx 5xx status code
            raise HTTPException(
                status_code=exc.response.status_code,
                detail=f"Error response from external API: {exc.response.text}",
            )


app = FastAPI(lifespan=lifespan)


@app.get("/posts", response_model=list[PostPublic])
async def get_posts(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    userId: int | None = None,
):  # TODO: figure out how to alias userId - user_id
    if userId:
        posts = session.exec(
            select(Post).where(Post.userId == userId).offset(offset).limit(limit)
        ).all()
    else:
        posts = session.exec(select(Post).offset(offset).limit(limit)).all()
    return posts


@app.get("/posts/{post_id}", response_model=PostPublic)
async def get_post(*, session: Session = Depends(get_session), post_id: int):
    post = session.get(Post, post_id)
    if not post:
        # post not found in internal db, search external API
        external_response = await external_api_get(f"{external_posts_url}{post_id}")
        if external_response.status_code == 200:
            # add post to db and return it
            exapi_post_data = external_response.json()
            new_post = Post.model_validate(exapi_post_data)
            session.add(new_post)
            session.commit()
            session.refresh(new_post)
            return new_post
        elif external_response.status_code == 404:
            # post not found in internal nor external api
            raise HTTPException(status_code=404, detail="Post not found")
        else:
            # raise from response
            raise HTTPException(
                status_code=external_response.status_code,
                detail=f"Error response from external API: {external_response.text}",
            )
    return post


@app.get("/users/{user_id}/posts", response_model=list[PostPublic])
async def get_user_posts(*, session: Session = Depends(get_session), userId: int):
    posts = session.exec(select(Post).where(Post.userId == userId)).all()
    return posts


@app.post("/posts", response_model=PostPublic)
async def create_post(*, session: Session = Depends(get_session), post: PostCreate):
    new_post = Post.model_validate(post)

    # validate userId from external api
    external_response = await external_api_get(f"{external_users_url}{new_post.userId}")
    if external_response.status_code == 200:
        session.add(new_post)
        session.commit()
        session.refresh(new_post)
        return new_post
    elif external_response.status_code == 404:
        raise HTTPException(
            status_code=404, detail=f"User with userId={new_post.userId} not found"
        )
    else:
        # 4xx 5xx
        raise HTTPException(
            status_code=external_response.status_code,
            detail=f"Error response from external API: {external_response.text}",
        )


@app.patch("/posts/{post_id}", response_model=PostPublic)
async def patch_post(
    *, session: Session = Depends(get_session), post_id: int, post: PostPatch
):
    db_post = session.get(Post, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    post_data = post.model_dump(exclude_unset=True)
    db_post.sqlmodel_update(post_data)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post


@app.delete("/posts/{post_id}")
async def delete_post(*, session: Session = Depends(get_session), post_id: int):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    session.delete(post)
    session.commit()
    return {"ok": True}
