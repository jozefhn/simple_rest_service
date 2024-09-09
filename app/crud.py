from sqlmodel import Session

from app.models.post import Post, PostCreate


def create_post(session: Session, post_create: PostCreate) -> Post:
    new_post = Post.model_validate(post_create)
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return new_post
