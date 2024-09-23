import unittest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

class TestOrders(unittest.TestCase):

    def setUp(self):
        # Очистити дані перед кожним тестом
        client.delete("/books/")
        client.delete("/orders/")

    # Тест для перевірки успішного оформлення замовлення
    def test_successful_order(self):
        client.post(
            "/books/",
            json={"id": 1, "title": "Book 1", "author": "Author A", "price": 10.0, "quantity": 5}
        )

        response = client.post(
            "/orders/",
            json={"id": 1, "book_id": 1, "customer_id": 123, "quantity": 2}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         {"id": 1, "book_id": 1, "customer_id": 123, "quantity": 2, "status": "Processing"})

    # Тест для перевірки замовлення при недостатній кількості книг
    def test_order_with_insufficient_stock(self):
        client.post(
            "/books/",
            json={"id": 2, "title": "Book 2", "author": "Author B", "price": 15.0, "quantity": 1}
        )

        response = client.post(
            "/orders/",
            json={"id": 2, "book_id": 2, "customer_id": 124, "quantity": 2}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Insufficient stock"})

    # Тест для перевірки замовлення книги, яка відсутня в інвентарі
    def test_order_with_book_not_in_inventory(self):
        response = client.post(
            "/orders/",
            json={"id": 3, "book_id": 999, "customer_id": 125, "quantity": 1}
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Book not found"})

    # Тест для перевірки зменшення кількості книг після замовлення
    def test_stock_decrease_after_order(self):
        client.post(
            "/books/",
            json={"id": 1, "title": "Book 1", "author": "Author A", "price": 10.0, "quantity": 5}
        )

        # Оформлення замовлення
        client.post(
            "/orders/",
            json={"id": 4, "book_id": 1, "customer_id": 126, "quantity": 1}
        )

        # Перевірка зменшення кількості
        response = client.get("/books/1")
        self.assertEqual(response.status_code, 200)
        book = response.json()
        self.assertEqual(book["quantity"], 4)

    # Тест для перевірки замовлення більше ніж наявна кількість книг
    def test_order_more_than_available_stock(self):
        client.post(
            "/books/",
            json={"id": 1, "title": "Book 1", "author": "Author A", "price": 10.0, "quantity": 5}
        )

        response = client.post(
            "/orders/",
            json={"id": 5, "book_id": 1, "customer_id": 127, "quantity": 10}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Insufficient stock"})


if __name__ == "__main__":
    unittest.main()
