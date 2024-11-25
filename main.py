import json
import os
from typing import List, Optional


class Book:
    """
    Класс, представляющий книгу в библиотеке.

    Атрибуты:
    - id: str - Уникальный идентификатор книги, генерируется автоматически.
    - title: str - Название книги.
    - author: str - Автор книги.
    - year: int - Год издания книги.
    - status: str - Статус книги ("в наличии" или "выдана").
    """

    def __init__(self, title: str, author: str, year: int):
        self.id: str = os.urandom(4).hex()
        self.title: str = title
        self.author: str = author
        self.year: int = year
        self.status: str = "в наличии"

    def to_dict(self) -> dict:
        """
        Преобразует объект книги в словарь для последующего сохранения.

        :return: Словарь с информацией о книге.
        """
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status,
        }


class Library:
    """
    Класс для управления библиотекой книг.

    Атрибуты:
    - data_file: str - Путь к файлу с данными о книгах.
    - books: List[Book] - Список книг в библиотеке.
    """

    def __init__(self, data_file: str):
        """
        Инициализирует библиотеку, загружая книги из файла данных, если он существует.

        :param data_file: Путь к файлу с данными о книгах.
        """
        self.data_file: str = data_file
        self.books: List[Book] = []
        self.load_books()

    def load_books(self) -> None:
        """
        Загружает книги из файла данных, если он существует.
        """
        if os.path.exists(self.data_file):
            with open(self.data_file, "r", encoding="utf-8") as file:
                books_data = json.load(file)
                self.books = [
                    Book(book["title"], book["author"], book["year"])
                    for book in books_data
                ]
                # Устанавливаем оригинальне исторические id и статус для каждой загруженной книги
                for book, book_data in zip(self.books, books_data):
                    book.id = book_data["id"]
                    book.status = book_data["status"]

    def save_books(self) -> None:
        """
        Сохраняет текущий список книг в файл данных.
        """
        with open(self.data_file, "w", encoding="utf-8") as file:
            json.dump(
                [book.to_dict() for book in self.books],
                file,
                indent=4,
                ensure_ascii=False,
            )

    def add_book(self, title: str, author: str, year: int) -> None:
        """
        Добавляет новую книгу в библиотеку, если книга с такими же данными ещё не существует.

        :param title: Название книги.
        :param author: Автор книги.
        :param year: Год издания книги.
        """
        # Проверка, существует ли уже такая книга
        for book in self.books:
            if book.title == title and book.author == author and book.year == year:
                print(
                    f"Книга с таким названием, автором и годом уже существует: {title}, {author}, {year}"
                )
                return

        book: Book = Book(title, author, year)
        self.books.append(book)
        self.save_books()
        print(f"Книга добавлена: {book.title} (ID: {book.id})")

    def remove_book(self, book_id: str) -> None:
        """
        Удаляет книгу из библиотеки по её ID.

        :param book_id: Иднтификатор книги.
        """
        book: Optional[Book] = self.find_book_by_id(book_id)
        if book:
            self.books.remove(book)
            self.save_books()
            print(f"Книга удалена: {book.title}")
        else:
            print(f"Книга с ID {book_id} не найдена.")

    def find_book_by_id(self, book_id: str) -> Optional[Book]:
        """
        Находит книгу по  ID.

        :param book_id: Уникальный идентификатор книги.
        :return: Объект книги, если книга найдена или None, если не найдена.
        """
        for book in self.books:
            if book.id == book_id:
                return book
        return None

    def search_books(self, search_term: str) -> None:
        """
        Ищет книги по названию, автору или году издания.

        :param search_term: Строка поиска (название, автор или год).
        """
        found_books: List[Book] = [
            book
            for book in self.books
            if search_term.lower() in book.title.lower()
            or search_term.lower() in book.author.lower()
            or search_term in str(book.year)
        ]
        if found_books:
            for book in found_books:
                self.display_book(book)
        else:
            print(f"Ничего не найдено по запросу: '{search_term}'")

    def display_books(self) -> None:
        """
        Отображает все книги в библиотеке.
        """
        if self.books:
            for book in self.books:
                self.display_book(book)
        else:
            print("Библиотека пуста.")

    def display_book(self, book: Book) -> None:
        """
        Отображает информацию о книге.

        :param book: Объект книги для отображения.
        """
        print(
            f"ID: {book.id}, Название: {book.title}, Автор: {book.author}, "
            f"Год: {book.year}, Статус: {book.status}"
        )

    def update_status(self, book_id: str, new_status: str) -> None:
        """
        Обновляет статус книги ("в наличии" или "выдана").

        :param book_id: Уникальный идентификатор книги.
        :param new_status: Новый статус книги ("в наличии" или "выдана").
        """
        book: Optional[Book] = self.find_book_by_id(book_id)
        if book:
            if new_status in ["в наличии", "выдана"]:
                book.status = new_status
                self.save_books()
                print(
                    f"Статус книги обновлен: {book.title} (новый статус: {book.status})"
                )
            else:
                print(
                    "Некорректный статус. Пожалуйста, введите 'в наличии' или 'выдана'."
                )
        else:
            print(f"Книга с ID {book_id} не найдена.")


def main() -> None:
    """
    Главная функция для работы с библиотекой через консольный интерфейс.
    """
    library: Library = Library("library.json")

    while True:
        # Отображение меню пользователя
        print("\n1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Поиск книги")
        print("4. Отображение всех книг")
        print("5. Изменение статуса книги")
        print("6. Выход")

        choice: str = input("\nВведите ваш выбор: ")

        # Логика меню
        if choice == "1":
            title: str = input("Название: ")
            author: str = input("Автор: ")
            year: int = int(input("Год издания: "))
            library.add_book(title, author, year)
        elif choice == "2":
            book_id: str = input("ID книги: ")
            library.remove_book(book_id)
        elif choice == "3":
            search_term: str = input("Поиск (название, автор, год): ")
            library.search_books(search_term)
        elif choice == "4":
            library.display_books()
        elif choice == "5":
            book_id: str = input("ID книги: ")
            new_status: str = input("Новый статус (в наличии/выдана): ")
            library.update_status(book_id, new_status)
        elif choice == "6":
            break
        else:
            print("Некорректный выбор. Пожалуйста, попробуйте еще раз.")


if __name__ == "__main__":
    main()
