from random import randrange
from typing import Optional
from fastapi import Body, FastAPI, Query, Request, Response, status
from contextlib import asynccontextmanager
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os
import json
    
# -----------------------------
# Load products JSON once at startup
# -----------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load products
    file_path = 'dataset/items.json'
    try:
        with open(file_path, 'r') as file:
            app.state.products = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        app.state.products = {}
    yield 

app = FastAPI(lifespan=lifespan)   

templates = Jinja2Templates(directory="dynamic/templates")

@app.get("/consultation-form", response_class=HTMLResponse)
async def consultation_form(request: Request):
    return templates.TemplateResponse("consultation-form.html", {"request": request})

@app.post("/submit-consultation", status_code=status.HTTP_201_CREATED)
async def submit_consultation(request: Request):
    data = await request.json()
    new_id = randrange(0, 100000)
    entry = {
        "id": new_id,
        "FULL NAME": data.get("name"),
        "PHONE NUMBER": data.get("phone"),
        "EMAIL": data.get("email")
    }
    file_path = "dataset/contact-invitations.json"
    print("Writing to:", os.path.abspath(file_path))
    print("Entry:", entry)
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            try:
                invitations = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                invitations = []
    else:
        invitations = []
    invitations.append(entry)
    with open(file_path, "w") as f:
        json.dump(invitations, f, indent=4)
    return JSONResponse(content={"message": "Consultation submitted successfully"})

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
# The Admin activities:
# ------------------------------

# -----------------------------
# Create a new product
# -----------------------------
@app.post("/Products",status_code=status.HTTP_201_CREATED)
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

@app.get("/explore", response_class=HTMLResponse)
def explore():
    file_path = os.path.join("dynamic/templates", "explore.html")
    with open(file_path, "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

# -----------------------------
# Delete a product
# -----------------------------
@app.delete("/Products/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int):
    for product_name, product_details in list(app.state.products.items()):
        if product_details.get("id") == id:
            del app.state.products[product_name]
            # Persist to JSON file
            with open('dataset/items.json', 'w') as file:
                json.dump(app.state.products, file, indent=4)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": f"Product with ID {id} not found."}
    )

# -----------------------------
# Update a product
# -----------------------------

@app.put("/Products/{id}", status_code=status.HTTP_200_OK)
def update_product(id: int, updated_product: Product):
    for product_name, product_details in app.state.products.items():
        if product_details.get("id") == id:
            updated_data = {
                "Price": updated_product.information.Price,
                "Description": updated_product.information.Description,
                "Quantity": updated_product.information.Quantity,
                "Category": updated_product.information.category,
                "is_available": updated_product.information.is_available,
                "id": id
            }
            app.state.products[product_name] = updated_data
            
            # Persist to JSON file
            with open('dataset/items.json', 'w') as file:
                json.dump(app.state.products, file, indent=4)
                
            return {"data": updated_data}
    
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": f"Product with ID {id} not found."}
    )