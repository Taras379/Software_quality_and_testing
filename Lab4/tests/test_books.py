import unittest
from fastapi.testclient import TestClient
from src.main import app

# Ініціалізація клієнта для тестування FastAPI
client = TestClient(app)

class TestBooks(unittest.TestCase):
    # Тест для перевірки створення нової книги
    def test_add_new_book(self):
        response = client.post(
            "/books/",
            json={"id": 1, "title": "Python Programming", "author": "John Doe", "price": 29.99, "quantity": 10}
        )
        # Перевірка, що статус-код відповіді 200 (успішно)
        self.assertEqual(response.status_code, 200)
        # Перевірка, що книга була додана з правильними даними
        self.assertEqual(response.json(), {
            "id": 1,
            "title": "Python Programming",
            "author": "John Doe",
            "price": 29.99,
            "quantity": 10,
            "description": None
        })

    # Тест для перевірки, що неможливо додати книгу з однаковим ID
    def test_duplicate_id(self):
        client.post(
            "/books/",
            json={"id": 2, "title": "Learning FastAPI", "author": "Jane Doe", "price": 39.99, "quantity": 5}
        )

        # Спроба додати іншу книгу з таким самим ID
        response = client.post(
            "/books/",
            json={"id": 2, "title": "Another Book", "author": "John Smith", "price": 19.99, "quantity": 15}
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Book with this ID already exists"})

    # Тест для перевірки оновлення інформації про книгу
    def test_update_book(self):
        # Оновлення першої книги
        response = client.put(
            "/books/1",
            json={"id": 1, "title": "Advanced Python Programming", "author": "John Doe", "price": 34.99, "quantity": 8}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "id": 1,
            "title": "Advanced Python Programming",
            "author": "John Doe",
            "price": 34.99,
            "quantity": 8,
            "description": None
        })

    # Тест для перевірки, що ISBN не можна змінювати
    def test_update_book_id_not_allowed(self):
        client.post(
            "/books/",
            json={"id": 3, "title": "Python Basics", "author": "Jane Doe", "price": 25.99, "quantity": 7}
        )

        # Спроба оновити книгу зі зміною ID
        response = client.put(
            "/books/3",
            json={"id": 99, "title": "Updated Python Basics", "author": "Jane Doe", "price": 29.99, "quantity": 5}
        )
        self.assertEqual(response.status_code, 400)
        book = client.get("/books/3").json()
        self.assertEqual(book["id"], 3)

    # Тест для перевірки видалення книги з інвентаря
    def test_delete_book(self):
        client.post(
            "/books/",
            json={"id": 4, "title": "To Delete", "author": "Author", "price": 19.99, "quantity": 5}
        )
        # Видалення книги
        response = client.delete("/books/4")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Book deleted successfully"})

        # Перевірка, що книга дійсно була видалена
        response = client.get("/books/4")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Book not found"})

    # Тест для перевірки видалення неіснуючої книги
    def test_delete_nonexistent_book(self):
        response = client.delete("/books/999")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Book not found"})

if __name__ == "__main__":
    unittest.main()
