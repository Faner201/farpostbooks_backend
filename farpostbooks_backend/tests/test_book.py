import pytest
from faker import Faker
from fastapi import FastAPI
from httpx import AsyncClient
from starlette import status

from farpostbooks_backend.db.dao.book_dao import BookDAO


@pytest.mark.anyio
async def test_get_book(
    fastapi_app: FastAPI,
    admin_client: AsyncClient,
    fake: Faker,
) -> None:
    """Тест эдпоинта и проверка существования книги и правильной работы БД."""
    dao = BookDAO()

    isbn = int(fake.isbn13().replace("-", ""))
    book = await dao.create_book_model(
        book_id=isbn,
        name=fake.sentence(nb_words=5),
        description=fake.sentence(nb_words=5),
        image=fake.image_url(),
        author=fake.name(),
        publish=fake.year(),
    )

    url = fastapi_app.url_path_for("search_book", book_id=isbn)
    response = await admin_client.get(url)
    json_response = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert json_response["id"] == book.id
    assert json_response["name"] == book.name
    assert json_response["description"] == book.description
    assert json_response["image"] == book.image


@pytest.mark.anyio
async def test_add(
    fastapi_app: FastAPI,
    admin_client: AsyncClient,
    fake: Faker,
) -> None:
    """Тест эндпоинта с добавлением данных о книги в БД."""
    isbn = int(fake.isbn13().replace("-", ""))
    url = fastapi_app.url_path_for("create_book", book_id=isbn)
    response = await admin_client.post(url)
    json_response = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert json_response["id"] == isbn
    assert json_response["name"] == "name"
    assert json_response["description"] == "description"
    assert json_response["image"] == "image"


@pytest.mark.anyio
async def test_scroll(
    fastapi_app: FastAPI,
    admin_client: AsyncClient,
    fake: Faker,
) -> None:
    """Тест эндпоинта для скроллинга главной странички."""
    dao = BookDAO()

    isbn = int(fake.isbn13().replace("-", ""))
    url = fastapi_app.url_path_for("get_books")

    response = await admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert not response.json()

    book = await dao.create_book_model(
        book_id=isbn,
        name=fake.sentence(nb_words=5),
        description=fake.sentence(nb_words=5),
        image=fake.image_url(),
        author=fake.name(),
        publish=fake.year(),
    )
    response = await admin_client.get(
        url,
        params={
            "limit": 1,
            "offset": 0,
        },
    )
    assert response.json()[0]["id"] == book.id

    response = await admin_client.get(url)
    assert response.json()[0]["id"] == book.id