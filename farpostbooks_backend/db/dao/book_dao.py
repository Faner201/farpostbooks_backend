from typing import List, Optional

from farpostbooks_backend.db.models.book_model import BookModel


class BookDAO:
    """Класс для доступа к таблице книг."""

    @staticmethod
    async def create_book_model(
        book_id: int,
        name: str,
        description: str,
        image: str,
        author: str,
        publish: str,
    ) -> BookModel:
        """
        Добавление новой книги.

        :param book_id: ISBN книги.
        :param name: Название книги.
        :param description: Описание книги.
        :param image: Фотография книги.
        :param author: Авторы книги.
        :param publish: Дата публикации книги.
        :return: Модель новой книги.
        """
        return (
            await BookModel.get_or_create(
                id=book_id,
                name=name,
                description=description,
                image=image,
                author=author,
                publish=publish,
            )
        )[0]

    @staticmethod
    async def delete_book_model(
        isbn: int,
    ) -> None:
        """
        Удаление книги.

        :param isbn: ISBN номер книги.
        """
        await BookModel.filter(id=isbn).delete()

    @staticmethod
    async def search_book(
        book_id: int,
    ) -> Optional[BookModel]:
        """
        Получить информацию о книге по его ISBN.

        :param book_id: ISBN книги.
        :return: stream of dummies.
        """
        return await BookModel.get_or_none(
            id=book_id,
        ).prefetch_related("user_books")

    @staticmethod
    async def get_books(
        limit: int = 10,
        offset: int = 0,
    ) -> List[BookModel]:
        """
        Выгрузка списка книг на главную страницу.

        :param limit: Максимальное количество выгружаемых книг.
        :param offset: Сдвиг от первой книги.
        :return: Список из книг со сдвигом.
        """
        return await BookModel.all().limit(limit).offset(offset)
