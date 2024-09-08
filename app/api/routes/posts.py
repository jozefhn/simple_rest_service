from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select

from app.api.deps import SessionDep
from app.api.routes.callbacks import posts_callback_router, users_callback_router
from app.api.utils import external_api_get
from app.core.config import settings
from app.models.post import Post, PostCreate, PostPatch, PostPublic

router = APIRouter()

external_users_url = settings.EXTERNAL_API_USERS
external_posts_url = settings.EXTERNAL_API_POSTS


@router.get("/", response_model=list[PostPublic])
async def get_posts(
    *,
    session: SessionDep,
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


@router.get(
    "/{post_id}", response_model=PostPublic, callbacks=posts_callback_router.routes
)
async def get_post(*, session: SessionDep, post_id: int):
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


@router.post("/", response_model=PostPublic, callbacks=users_callback_router.routes)
async def create_post(*, session: SessionDep, post: PostCreate):
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


@router.patch("/{post_id}", response_model=PostPublic)
async def patch_post(*, session: SessionDep, post_id: int, post: PostPatch):
    db_post = session.get(Post, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    post_data = post.model_dump(exclude_unset=True)
    db_post.sqlmodel_update(post_data)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post


@router.delete("/{post_id}")
async def delete_post(*, session: SessionDep, post_id: int):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    session.delete(post)
    session.commit()
    return {"ok": True}
