import random
import string

from sqlmodel import Session

from app import crud
from app.models.post import Post, PostCreate


def rand_str(length: int = 16) -> str:
    return "".join(random.choices(string.ascii_letters, k=length))


def create_random_post(db: Session) -> Post:
    title = rand_str(8)
    body = rand_str(16)
    userId = 1
    new_post = PostCreate(title=title, body=body, userId=userId)
    return crud.create_post(db, new_post)
