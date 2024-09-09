from fastapi.testclient import TestClient
from sqlmodel import Session

# from app.core.config import settings
from app.tests.utils import create_random_post


def test_create_post(client: TestClient) -> None:
    data = {"title": "Foo", "body": "bar", "userId": 1}
    response = client.post("/posts/", json=data)

    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["body"] == data["body"]
    assert content["userId"] == data["userId"]
    assert "id" in content


def test_read_item(client: TestClient, db: Session) -> None:
    new_post = create_random_post(db)
    response = client.get(f"/posts/{new_post.id}")

    assert response.status_code == 200
    content = response.json()
    print(f"\n\n{new_post}")
    print(f"{content}\n\n")
    assert content["title"] == new_post.title
    assert content["body"] == new_post.body
    assert content["userId"] == new_post.userId
    assert content["id"] == new_post.id


def test_read_item_not_found() -> None:
    pass


def test_read_items() -> None:
    pass


def test_update_item() -> None:
    pass


def test_update_item_not_found() -> None:
    pass


def test_delete_item() -> None:
    pass


def test_delete_item_not_found() -> None:
    pass
