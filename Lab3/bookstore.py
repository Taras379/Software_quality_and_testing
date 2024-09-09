import uuid

class Bookstore:
    def __init__(self):
        self.inventory = {}
        self.orders = {}
        self.discounts = {}

    # Функція 1: Керування інвентарем книг
    def book_exists(self, isbn: str) -> bool:
        # Перевіряє, чи існує книга з таким ISBN в інвентарі
        return isbn in self.inventory

    def add_book(self, title: str, author: str, isbn: str, price: float, quantity: int):
        # Додає книгу до інвентарю, якщо такої книги ще немає в базі
        if self.book_exists(isbn):
            raise ValueError("Book with this ISBN already exists")
        self.inventory[isbn] = {
            "title": title,
            "author": author,
            "price": price,
            "quantity": quantity
        }

    # Функція 2: Обробка покупок книг
    def is_quantity_sufficient(self, book: dict, quantity: int) -> bool:
        # Перевіряє, чи достатньо кількість книг для покупки
        return quantity <= book["quantity"]

    def purchase_book(self, isbn: str, quantity: int) -> float:
        # Оформлює покупку книги
        if not self.book_exists(isbn):
            raise ValueError("Book not found")

        book = self.inventory[isbn]

        if not self.is_quantity_sufficient(book, quantity):
            raise ValueError("Insufficient quantity")

        book["quantity"] -= quantity
        return book["price"] * quantity

    # Функція 3: Відстеження замовлень клієнтів
    def validate_order_items(self, items: list):
        # Перевіряє валідність книг в замовленні (існування та кількість)
        for isbn, quantity in items:
            if not self.book_exists(isbn):
                raise ValueError("Book not found")
            book = self.inventory[isbn]
            if not self.is_quantity_sufficient(book, quantity):
                raise ValueError("Insufficient quantity")

    def calculate_total_amount(self, items: list) -> float:
        # Обчислює загальну вартість замовлення
        total_amount = 0
        for isbn, quantity in items:
            total_amount += self.inventory[isbn]["price"] * quantity
        return total_amount

    def create_order(self, customer_name: str, address: str, contact_info: str, items: list) -> dict:
        # Створює нове замовлення
        self.validate_order_items(items)

        total_amount = self.calculate_total_amount(items)
        order_items = {isbn: {"quantity": quantity, "price": self.inventory[isbn]["price"]} for isbn, quantity in items}

        order_id = str(uuid.uuid4())  # унікальний ідентифікатор замовлення
        self.orders[order_id] = {
            "customer_name": customer_name,
            "contact_info": f"{address}, {contact_info}",
            "items": order_items,
            "total_amount": total_amount,
            "status": "Processing"
        }

        order_response = self.orders[order_id]
        order_response["order_id"] = order_id

        return order_response

    def update_order_status(self, order_id: str, status: str):
        # Оновлює статус замовлення
        if order_id not in self.orders:
            raise ValueError("Order not found")

        self.orders[order_id]["status"] = status

    # Функція 4: Пошук книг
    def search_books(self, title=None, author=None, isbn=None):
        results = []
        for book_isbn, book in self.inventory.items():
            # Перевірка умов пошуку
            title_match = title is None or title.lower() in book["title"].lower()
            author_match = author is None or author.lower() in book["author"].lower()
            isbn_match = isbn is None or isbn == book_isbn

            # Додавання результатів пошуку
            if title_match and author_match and isbn_match:
                results.append({
                    "title": book["title"],
                    "author": book["author"],
                    "isbn": book_isbn,
                    "price": book["price"],
                    "quantity": book["quantity"]
                })
        return results

    # Функція 5: Управління знижками
    def add_discount(self, isbn: str, discount_percentage: float):
        # Додавання знижки
        if not 0 <= discount_percentage <= 100:
            raise ValueError("Discount must be between 0 and 100")

        if not self.book_exists(isbn):
            raise ValueError("Book not found")

        self.discounts[isbn] = discount_percentage

    def get_discount(self, isbn: str) -> float:
        # Отримання знижки
        return self.discounts.get(isbn, 0)

    def apply_discounts(self, items: list) -> float:
        # Застосування знижок до загальної вартості замовлення
        total_amount = 0
        for isbn, quantity in items:
            if not self.book_exists(isbn):
                raise ValueError(f"Book with ISBN {isbn} not found")
            book = self.inventory[isbn]
            price = book["price"]
            discount = self.get_discount(isbn)
            final_price = price * (1 - discount / 100)
            total_amount += final_price * quantity
        return total_amount