import unittest
from unittest.mock import patch, mock_open
import json
from main import Book, Library

class TestLibraryManagement(unittest.TestCase):
    def setUp(self):
        # Создаем экземпляр библиотеки для тестов
        self.library = Library('test_library.json')
        self.library.books = []
        self.book_data = [
            {"id": "1a2b3c4d", "title": "Война и мир", "author": "Лев Толстой", "year": 1869, "status": "в наличии"},
            {"id": "2b3c4d5e", "title": "Преступление и наказание", "author": "Федор Достоевский", "year": 1866, "status": "выдана"}
        ]

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([]))
    @patch("os.path.exists", return_value=True)
    def test_load_books(self, mock_exists, mock_open_func):
        # Тест загрузки книг из файла
        with patch("json.load", return_value=self.book_data):
            self.library.load_books()
        self.assertEqual(len(self.library.books), 2)
        self.assertEqual(self.library.books[0].title, "Война и мир")
        self.assertEqual(self.library.books[1].author, "Федор Достоевский")

    @patch("builtins.open", new_callable=mock_open)
    def test_save_books(self, mock_open_func):
        # Тест сохранения книг в файл
        self.library.books = [Book("Война и мир", "Лев Толстой", 1869)]
        # Поскольку json.dump вызывает метод write несколько раз, проверяем, что он был вызван хотя бы один раз

        self.library.save_books()
        mock_open_func().write.assert_called()

    def test_add_book(self):
        # Тест добавления новой книги
        # Очищаем список книг перед тестированием
        self.library.books = []
        self.library.add_book("Анна Каренина", "Лев Толстой", 1877)
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0].title, "Анна Каренина")

    def test_add_existing_book(self):
        # Тест добавления уже существующей книги
        self.library.books = [Book("Война и мир", "Лев Толстой", 1869)]
        with patch("builtins.print") as mocked_print:
            self.library.add_book("Война и мир", "Лев Толстой", 1869)
            mocked_print.assert_called_with("Книга с таким названием, автором и годом уже существует: Война и мир, Лев Толстой, 1869")
        self.assertEqual(len(self.library.books), 1)

    def test_remove_book(self):
        # Тест удаления книги по ID
        book = Book("Война и мир", "Лев Толстой", 1869)
        book.id = "1a2b3c4d"
        self.library.books = [book]
        self.library.remove_book("1a2b3c4d")
        self.assertEqual(len(self.library.books), 0)

    def test_remove_nonexistent_book(self):
        # Тест удаления несуществующей книги
        with patch("builtins.print") as mocked_print:
            self.library.remove_book("nonexistent_id")
            mocked_print.assert_called_with("Книга с ID nonexistent_id не найдена.")

    def test_find_book_by_id(self):
        # Тест поиска книги по ID
        book = Book("Преступление и наказание", "Федор Достоевский", 1866)
        book.id = "2b3c4d5e"
        self.library.books = [book]
        found_book = self.library.find_book_by_id("2b3c4d5e")
        self.assertIsNotNone(found_book)
        self.assertEqual(found_book.title, "Преступление и наказание")

    def test_search_books(self):
        # Тест поиска книг по автору, названию или году
        self.library.books = [
            Book("Война и мир", "Лев Толстой", 1869),
            Book("Преступление и наказание", "Федор Достоевский", 1866)
        ]
        with patch("builtins.print") as mocked_print:
            self.library.search_books("Толстой")
            mocked_print.assert_called()

    def test_update_status(self):
        # Тест обновления статуса книги
        book = Book("Война и мир", "Лев Толстой", 1869)
        book.id = "1a2b3c4d"
        self.library.books = [book]
        self.library.update_status("1a2b3c4d", "выдана")
        self.assertEqual(self.library.books[0].status, "выдана")

    def test_update_status_invalid(self):
        # Тест обновления статуса с некорректным значением
        book = Book("Война и мир", "Лев Толстой", 1869)
        book.id = "1a2b3c4d"
        self.library.books = [book]
        with patch("builtins.print") as mocked_print:
            self.library.update_status("1a2b3c4d", "неправильный статус")
            mocked_print.assert_called_with("Некорректный статус. Пожалуйста, введите 'в наличии' или 'выдана'.")

if __name__ == "__main__":
    unittest.main()
