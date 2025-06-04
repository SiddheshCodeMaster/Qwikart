from random import randrange
from typing import Optional
from fastapi import Body, FastAPI, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import json

app = FastAPI()

# -----------------------------
# Define data models using Pydantic
# -----------------------------
class ProductInfo(BaseModel):
    Price: float
    Description: str
    Quantity: int
    is_available: bool
    category: str
    id: Optional[int]

class Product(BaseModel):
    product_name: str
    information: ProductInfo

# -----------------------------
# Mount static folder for HTML rendering
# -----------------------------
app.mount("/dynamic", StaticFiles(directory="dynamic"), name="dynamic")

# -----------------------------
# Load products JSON once at startup
# -----------------------------
@app.on_event("startup")
def load_products():
    file_path = 'dataset/items.json'
    try:
        with open(file_path, 'r') as file:
            app.state.products = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        app.state.products = {}

# -----------------------------
# Welcome page endpoint
# -----------------------------
@app.get("/welcomeQwikart", response_class=HTMLResponse)
def root():
    file_path = os.path.join("dynamic/templates", "welcome.html")
    with open(file_path, "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

# -----------------------------
# Get all products
# -----------------------------
@app.get("/get_all_products")
def get_products():
    return {"product_data": app.state.products}

# -----------------------------
# Get products by category
# -----------------------------
@app.get("/Products")
async def get_products_by_category(category: str = Query(..., description="Category to filter by")):
    data = app.state.products
    filtered_products = {
        name: details for name, details in data.items()
        if details.get("Category", "").lower() == category.lower()
    }

    if not filtered_products:
        return JSONResponse(
            status_code=404,
            content={"message": f"No products found in category: {category}"}
        )
    
    return {"products": filtered_products}

# -----------------------------
# Get product by ID
# -----------------------------
@app.get("/Products/{id}")
def get_product(id: int):
    for product_name, product_details in app.state.products.items():
        if product_details.get("id") == id:
            return {"product_detail": {product_name: product_details}}
    return {"error": f"Product with ID {id} not found."}

# -----------------------------
# Create a new product
# -----------------------------
@app.post("/Products")
def create_products(new_product: Product):
    new_id = randrange(0, 100000)
    product_data = {
        "Price": new_product.information.Price,
        "Description": new_product.information.Description,
        "Quantity": new_product.information.Quantity,
        "Category": new_product.information.category,
        "is_available": new_product.information.is_available,
        "id": new_id
    }

    # Update in-memory products
    app.state.products[new_product.product_name] = product_data

    # Persist to JSON file
    with open('dataset/items.json', 'w') as file:
        json.dump(app.state.products, file, indent=4)

    return {"data": product_data}
