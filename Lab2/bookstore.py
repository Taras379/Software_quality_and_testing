class Bookstore:
    def __init__(self):
        self.inventory = {}

    def add_book(self, title: str, author: str, price: float, quantity: int):
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")
        if price < 0:
            raise ValueError("Price cannot be negative")
        if title in self.inventory:
            self.inventory[title]["quantity"] += quantity
        else:
            self.inventory[title] = {
                "author": author,
                "price": price,
                "quantity": quantity
            }

    def remove_book(self, title: str):
        if title in self.inventory:
            del self.inventory[title]

    def search_book(self, title: str) -> dict:
        if not title:
            return None
        if title in self.inventory:
            return {
                "title": title,
                "author": self.inventory[title]["author"],
                "price": self.inventory[title]["price"],
                "quantity": self.inventory[title]["quantity"]
            }
        return None

    def purchase_book(self, title: str, quantity: int) -> float:
        if title not in self.inventory:
            raise ValueError("Book not found")
        if self.inventory[title]["quantity"] == 0:
            raise ValueError("Book is out of stock")
        if self.inventory[title]["quantity"] < quantity:
            raise ValueError("Not enough books in inventory")
        self.inventory[title]["quantity"] -= quantity
        return self.inventory[title]["price"] * quantity

    def inventory_value(self) -> float:
        total = 0.0
        for book in self.inventory.values():
            total += book["price"] * book["quantity"]
        return total

    def apply_discount(self, title: str, discount_percentage: float):
        if title in self.inventory and 0 <= discount_percentage <= 100:
            self.inventory[title]['price'] *= (1 - discount_percentage / 100)

    def apply_promotion(self, promotion_details: dict):
        for title, discount in promotion_details.items():
            self.apply_discount(title, discount)


