import unittest
from bookstore import Bookstore

class TestBookstore(unittest.TestCase):

    def setUp(self):
        self.store = Bookstore()
        # Очистити інвентар перед кожним тестом
        self.store.inventory = {}
        # Книги для тестування
        self.store.add_book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565", 10.99, 5)
        self.store.add_book("1984", "George Orwell", "9780451524935", 8.99, 3)

    # Функція 1: Керування інвентарем книг
    def test_add_book_success(self):
        self.store.add_book("To Kill a Mockingbird", "Harper Lee", "9780061120084", 12.99, 10)
        self.assertIn("9780061120084", self.store.inventory)
        self.assertEqual(self.store.inventory["9780061120084"]["title"], "To Kill a Mockingbird")

    def test_add_book_duplicate_isbn(self):
        with self.assertRaises(ValueError):
            self.store.add_book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565", 10.99, 5)

    # Функція 2: Обробка покупок книг
    def test_purchase_book_success(self):
        total_price = self.store.purchase_book("9780743273565", 2)
        self.assertEqual(total_price, 21.98)
        self.assertEqual(self.store.inventory["9780743273565"]["quantity"], 3)

    def test_purchase_book_insufficient_quantity(self):
        with self.assertRaises(ValueError):
            self.store.purchase_book("9780451524935", 5)

    def test_purchase_nonexistent_book(self):
        with self.assertRaises(ValueError):
            self.store.purchase_book("0000000000000", 1)

    def test_purchase_book_zero_quantity(self):
        self.store.purchase_book("9780451524935", 3)
        with self.assertRaises(ValueError):
            self.store.purchase_book("9780451524935", 1)

    # Функція 3: Відстеження замовлень клієнтів
    def test_create_order_success(self):
        self.store.purchase_book("9780743273565", 2)
        order = self.store.create_order("John Doe", "123 Main St", "555-1234", [("9780743273565", 2)])
        self.assertEqual(order["customer_name"], "John Doe")
        self.assertEqual(order["contact_info"], "123 Main St, 555-1234")
        self.assertIn("9780743273565", order["items"])
        self.assertEqual(order["items"]["9780743273565"]["quantity"], 2)
        self.assertEqual(order["status"], "Processing")

    def test_order_status_update(self):
        self.store.purchase_book("9780743273565", 2)
        order = self.store.create_order("Jane Doe", "456 Elm St", "555-5678", [("9780743273565", 2)])
        self.store.update_order_status(order["order_id"], "Shipped")
        self.assertEqual(order["status"], "Shipped")

    def test_order_details(self):
        self.store.purchase_book("9780743273565", 2)
        order = self.store.create_order("Alice Smith", "789 Oak St", "555-8765", [("9780743273565", 2)])
        self.assertEqual(order["total_amount"], 21.98)
        self.assertEqual(order["items"]["9780743273565"]["price"], 10.99)

    def test_create_order_insufficient_quantity(self):
        with self.assertRaises(ValueError):
            self.store.create_order("Bob Brown", "101 Pine St", "555-9999", [("9780451524935", 5)])

    # Функція 4: Пошук книг
    def test_search_by_title(self):
        results = self.store.search_books(title="1984")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "1984")

    def test_search_by_author(self):
        results = self.store.search_books(author="F. Scott Fitzgerald")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["author"], "F. Scott Fitzgerald")

    def test_search_by_isbn(self):
        results = self.store.search_books(isbn="9780743273565")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["isbn"], "9780743273565")

    def test_search_combined(self):
        results = self.store.search_books(title="The Great Gatsby", author="F. Scott Fitzgerald")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "The Great Gatsby")
        self.assertEqual(results[0]["author"], "F. Scott Fitzgerald")

    def test_search_no_results(self):
        results = self.store.search_books(title="Nonexistent Book")
        self.assertEqual(len(results), 0)

    # Функція 5: Управління знижками
    def test_add_discount(self):
        self.store.add_discount("9780743273565", 15)
        discount = self.store.get_discount("9780743273565")
        self.assertEqual(discount, 15)

    def test_add_discount_invalid(self):
        with self.assertRaises(ValueError):
            self.store.add_discount("9780743273565", 110)

    def test_add_discount_update_existing(self):
        self.store.add_discount("9780743273565", 15)
        self.store.add_discount("9780743273565", 20)
        discount = self.store.get_discount("9780743273565")
        self.assertEqual(discount, 20)

    def test_get_discount_no_discount(self):
        discount = self.store.get_discount("9780451524935")
        self.assertEqual(discount, 0)

    def test_apply_discounts(self):
        self.store.add_discount("9780743273565", 15)  # 15% знижка
        self.store.add_discount("9780451524935", 10)  # 10% знижка

        items = [("9780743273565", 2), ("9780451524935", 1)]
        total_amount = self.store.apply_discounts(items)
        expected_amount = (10.99 * 0.85 * 2) + (8.99 * 0.90)
        self.assertAlmostEqual(total_amount, expected_amount)

    def test_apply_discounts_no_items(self):
        items = []
        total_amount = self.store.apply_discounts(items)
        self.assertEqual(total_amount, 0)


if __name__ == '__main__':
    unittest.main()