from fastapi import APIRouter

from app.core.config import settings
from app.models.callbacks import ExternalPost, ExternalUser

users_callback_router = APIRouter()
posts_callback_router = APIRouter()


@users_callback_router.get(
    settings.EXTERNAL_API_USERS + "{$request.body.userId}", response_model=ExternalUser
)
def get_external_user(userId: int):  # noqa: ARG001
    pass


@posts_callback_router.get(
    settings.EXTERNAL_API_POSTS + "{$request.post_id}", response_model=ExternalPost
)
def get_external_post(postId: int):  # noqa: ARG001
    pass
