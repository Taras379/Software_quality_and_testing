from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from fastapi import HTTPException

app = FastAPI()

# Інвентар книг та замовлень
books = []
orders = []

class Book(BaseModel):
    id: int
    title: str
    author: str
    price: float
    quantity: int
    description: Optional[str] = None

class Order(BaseModel):
    id: int
    book_id: int
    customer_id: int
    quantity: int
    status: str = "Processing"


'''КЕРУВАННЯ ІНВЕНТАРЕМ КНИГ'''
# Додавання нової книги до інвентаря
@app.post("/books/", response_model=Book)
def add_book(book: Book):
    for existing_book in books:
        if existing_book["id"] == book.id:
            raise HTTPException(status_code=400, detail="Book with this ID already exists")
    books.append(book.model_dump())
    return book

# Оновлення інформації про книгу (ціна, кількість, опис)
@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, updated_book: Book):
    for idx, book in enumerate(books):
        if book["id"] == book_id:
            updated_book_dict = updated_book.model_dump()
            if updated_book_dict["id"] != book_id:
                raise HTTPException(status_code=400, detail="Cannot change book ID")
            books[idx] = updated_book_dict
            return updated_book
    raise HTTPException(status_code=404, detail="Book not found")

# Отримання інформації про книгу за її ID або всі книги
@app.get("/books/", response_model=List[Book])
def get_books():
    return books

@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

# Видалення книги з інвентаря
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    global books
    initial_length = len(books)
    books = [book for book in books if book["id"] != book_id]
    if len(books) == initial_length:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}


'''ОБРОБКА ПОКУПОК КНИГ'''
# Додавання нового замовлення на покупку книги
@app.post("/orders/", response_model=Order)
def add_order(order: Order):

    book = next((b for b in books if b["id"] == order.book_id), None)

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    if book["quantity"] < order.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    # Зменшення кількості книг в інвентарі
    book["quantity"] -= order.quantity

    orders.append(order.model_dump())
    return order

# Оновлення статусу замовлення
@app.put("/orders/{order_id}", response_model=Order)
def update_order(order_id: int, updated_order: Order):
    valid_statuses = ["Processing", "Shipped", "Completed"]

    # Перевірка наявності замовлення
    for idx, order in enumerate(orders):
        if order["id"] == order_id:
            # Перевірка валідності статусу
            if updated_order.status not in valid_statuses:
                raise HTTPException(status_code=400, detail="Invalid status")

            # Оновлення тільки статусу
            orders[idx]["status"] = updated_order.status
            return orders[idx]

    raise HTTPException(status_code=404, detail="Order not found")

# Отримання інформації про замовлення за ID
@app.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: int):
    for order in orders:
        if order["id"] == order_id:
            return order
    raise HTTPException(status_code=404, detail="Order not found")


'''ВІДСТЕЖЕННЯ ЗАМОВЛЕНЬ КЛІЄНТІВ'''
# Перегляд замовлень клієнта за його ID
@app.get("/orders/customer/{customer_id}", response_model=dict)
def get_customer_orders(customer_id: int):
    customer_orders = [order for order in orders if order["customer_id"] == customer_id]
    if not customer_orders:
        raise HTTPException(status_code=404, detail="No orders found for this customer")
    return {"orders": customer_orders}

# Статуси замовлень (на обробці, відправлено, виконано)
@app.get("/orders/status/{status}", response_model=dict)
def get_orders_by_status(status: str):
    valid_statuses = ["Processing", "Shipped", "Completed"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Invalid status")

    orders_by_status = [order for order in orders if order["status"] == status]
    return {"orders": orders_by_status}
