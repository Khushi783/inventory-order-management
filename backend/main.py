# inventory-order-management
Full-stack Inventory &amp; Order Management System (FastAPI + React + PostgreSQL + Docker).
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Models
class Product(BaseModel):
    id: int | None = None
    name: str
    sku: str
    price: float
    quantity: int

class Customer(BaseModel):
    id: int | None = None
    full_name: str
    email: str
    phone: str

class Order(BaseModel):
    id: int | None = None
    customer_id: int
    product_id: int
    quantity: int
    total_amount: float | None = None

# In-memory storage (replace with DB later)
products: List[Product] = []
customers: List[Customer] = []
orders: List[Order] = []

@app.post("/products")
def create_product(product: Product):
    if any(p.sku == product.sku for p in products):
        raise HTTPException(status_code=400, detail="SKU must be unique")
    products.append(product)
    return product

@app.get("/products")
def get_products():
    return products

@app.post("/customers")
def create_customer(customer: Customer):
    if any(c.email == customer.email for c in customers):
        raise HTTPException(status_code=400, detail="Email must be unique")
    customers.append(customer)
    return customer

@app.post("/orders")
def create_order(order: Order):
    product = next((p for p in products if p.id == order.product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.quantity < order.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    product.quantity -= order.quantity
    order.total_amount = product.price * order.quantity
    orders.append(order)
    return order
