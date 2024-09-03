import pytest
from bookstore import Bookstore

# Тест додавання книг
def test_add_book():
    store = Bookstore()
    store.add_book("The Catcher in the Rye", "J.D. Salinger", 10.99, 5)
    store.add_book("The Catcher in the Rye", "J.D. Salinger", 10.99, 3)

    assert store.inventory["The Catcher in the Rye"]["quantity"] == 8

# Тест видалення книг
def test_remove_book():
    store = Bookstore()
    store.add_book("1984", "George Orwell", 8.99, 10)
    store.remove_book("1984")

    assert "1984" not in store.inventory

    # Спроба видалити книгу, якої немає в інвентарі
    store.remove_book("Nonexistent Book")
    assert "Nonexistent Book" not in store.inventory

# Тест пошуку книг
def test_search_book():
    store = Bookstore()
    store.add_book("Brave New World", "Aldous Huxley", 12.99, 7)

    result = store.search_book("Brave New World")
    assert result == {
        "title": "Brave New World",
        "author": "Aldous Huxley",
        "price": 12.99,
        "quantity": 7
    }

    # Пошук книги, якої немає в інвентарі
    result = store.search_book("Nonexistent Book")
    assert result is None

#  Тест покупки книг
def test_purchase_book():
    store = Bookstore()
    store.add_book("To Kill a Mockingbird", "Harper Lee", 14.99, 10)

    # Покупка доступної кількості книг
    total_price = store.purchase_book("To Kill a Mockingbird", 3)
    assert total_price == 44.97
    assert store.inventory["To Kill a Mockingbird"]["quantity"] == 7

    # Спроба купити більше книг, ніж є в наявності
    with pytest.raises(ValueError):
        store.purchase_book("To Kill a Mockingbird", 8)

    # Спроба купити книгу, якої немає в інвентарі
    with pytest.raises(ValueError):
        store.purchase_book("Nonexistent Book", 1)

# Тест обчислення вартості інвентарю
def test_inventory_value():
    store = Bookstore()
    store.add_book("Book A", "Author A", 20.00, 2)
    store.add_book("Book B", "Author B", 15.00, 3)

    total_value = store.inventory_value()
    assert total_value == 85.00

#Обробка крайніх випадків
def test_add_book_negative_quantity():
    store = Bookstore()
    with pytest.raises(ValueError):
        store.add_book("Negative Quantity Book", "Author", 10.99, -5)

def test_add_book_negative_price():
    store = Bookstore()
    with pytest.raises(ValueError):
        store.add_book("Negative Price Book", "Author", -10.99, 5)

def test_purchase_book_with_zero_stock():
    store = Bookstore()
    store.add_book("Zero Stock Book", "Author", 10.99, 0)
    with pytest.raises(ValueError):
        store.purchase_book("Zero Stock Book", 1)

def test_remove_nonexistent_book():
    store = Bookstore()
    store.remove_book("Nonexistent Book")  # No error should be raised

def test_search_book_with_empty_title():
    store = Bookstore()
    result = store.search_book("")
    assert result is None

def test_search_book_with_null_title():
    store = Bookstore()
    result = store.search_book(None)
    assert result is None

# Тест для знижок
def test_apply_discount():
    store = Bookstore()
    store.add_book("1984", "George Orwell", 15.00, 10)
    store.apply_discount("1984", 20)
    assert store.inventory["1984"]["price"] == 12.00

# Тест для акцій
def test_apply_promotion():
    store = Bookstore()
    store.add_book("Brave New World", "Aldous Huxley", 20.00, 5)
    store.add_book("1984", "George Orwell", 15.00, 10)
    promotions = {"Brave New World": 10, "1984": 5}
    store.apply_promotion(promotions)
    assert store.inventory["Brave New World"]["price"] == 18.00
    assert store.inventory["1984"]["price"] == 14.25

