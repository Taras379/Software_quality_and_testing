import unittest
from fastapi.testclient import TestClient
from src.main import app, books, orders

client = TestClient(app)

class TestCustomerOrders(unittest.TestCase):

    def setUp(self):
        # Ініціалізація книг та замовлень перед кожним тестом
        books.clear()
        orders.clear()

        # Додавання тестових даних
        books.append({
            "id": 1,
            "title": "Test Book",
            "author": "Author A",
            "price": 10.0,
            "quantity": 100,
            "description": "A test book"
        })

    # Тест на створення нового замовлення
    def test_create_new_order(self):
        response = client.post("/orders/", json={
            "id": 1,
            "book_id": 1,
            "customer_id": 1,
            "quantity": 1,
            "status": "Processing"
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()

        # Перевірка, що замовлення створено з унікальним ідентифікатором
        self.assertEqual(data["id"], 1)

        # Перевірка, що всі необхідні деталі включені у замовлення
        self.assertEqual(data["book_id"], 1)
        self.assertEqual(data["customer_id"], 1)
        self.assertEqual(data["quantity"], 1)
        self.assertEqual(data["status"], "Processing")

    # Тест на оновлення статусу замовлення
    def test_update_order_status(self):
        # Створення нового замовлення
        client.post("/orders/", json={
            "id": 1,
            "book_id": 1,
            "customer_id": 1,
            "quantity": 1,
            "status": "Processing"
        })

        # Оновлення статусу замовлення
        response = client.put("/orders/1", json={
            "id": 1,
            "book_id": 1,
            "customer_id": 1,
            "quantity": 1,
            "status": "Shipped"
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()

        # Перевірка, що статус замовлення змінився
        self.assertEqual(data["status"], "Shipped")

    # Тест на отримання замовлень клієнта
    def test_get_orders_for_customer(self):
        # Створення двох замовлень для одного клієнта
        client.post("/orders/", json={
            "id": 1,
            "book_id": 1,
            "customer_id": 1,
            "quantity": 1,
            "status": "Processing"
        })

        client.post("/orders/", json={
            "id": 2,
            "book_id": 1,
            "customer_id": 1,
            "quantity": 2,
            "status": "Processing"
        })

        # Отримання всіх замовлень клієнта
        response = client.get("/orders/customer/1")
        self.assertEqual(response.status_code, 200)
        data = response.json()

        # Перевірка, що клієнт може переглянути всі свої попередні замовлення
        self.assertEqual(len(data["orders"]), 2)
        self.assertEqual(data["orders"][0]["id"], 1)
        self.assertEqual(data["orders"][1]["id"], 2)

if __name__ == "__main__":
    unittest.main()
