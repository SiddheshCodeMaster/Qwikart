from random import randrange
from typing import Optional
from fastapi import Body, FastAPI, Query

from pydantic import BaseModel

# Reading the welcome page:
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os
import json

app = FastAPI()

# Pydantic BaseModel for product information
class ProductInfo(BaseModel):
    Price: float
    Description: str
    Quantity: int
    is_available : bool
    category : str
    id : Optional[int]

# Pydantic BaseModel for new product data
class Product(BaseModel):
    product_name: str
    information: ProductInfo

# Mount the static folder for serving static files
app.mount("/dynamic", StaticFiles(directory="dynamic"), name="dynamic")

@app.get("/welcomeQwikart", response_class=HTMLResponse)
def root():
     # Get the path of the HTML file
    file_path = os.path.join("dynamic/templates", "welcome.html")
    
    # Read the HTML file content
    with open(file_path, "r") as file:
        html_content = file.read()
    
    return HTMLResponse(content=html_content)

# Endpoint to retrieve all products
@app.get("/get_all_products")
def get_products():
    
    # Load the product data from items.json file
    with open('dataset/items.json', 'r') as file:
        products = json.load(file)
    
    # Return the data in the desired format
    return {
        "product_data": products
	}

# Endpoint to retrieve products based on Category
@app.get("/Products")
async def get_products_by_category(category: str = Query(..., description="Category to filter by")):
    filtered_products = {}

    # Load the product data from items.json file
    with open('dataset/items.json', 'r') as file:
        data = json.load(file)

    for product_name, details in data.items():
        # Some products might not have a Category field
        product_category = details.get("Category")
        if product_category and product_category.lower() == category.lower():
            filtered_products[product_name] = details

    if not filtered_products:
        return JSONResponse(
            status_code=404,
            content={"message": f"No products found in category: {category}"}
        )
    
    return {"products": filtered_products}

@app.get("/products")
async def get_products_by_category(category: str = Query(..., description="Category to filter by")):
    filtered_products = {}

    for product_name, details in data.items():
        # Some products might not have a Category field
        product_category = details.get("Category")
        if product_category and product_category.lower() == category.lower():
            filtered_products[product_name] = details

    if not filtered_products:
        return JSONResponse(
            status_code=404,
            content={"message": f"No products found in category: {category}"}
        )
    
    return {"products": filtered_products}

# Endpoint to create new products
@app.post("/Products")
def create_products(new_product: Product):
    # Read the existing product data
    file_path = 'dataset/items.json'
    with open(file_path, 'r') as file:
        products = json.load(file)

    # Add the new product to the data
    products[new_product.product_name] = {
        "Price": new_product.information.Price,
        "Description": new_product.information.Description,
        "Quantity": new_product.information.Quantity,
        "is_available": new_product.information.is_available,
        "id" : randrange(0,100000)
    }

    # Write updated data back to the file
    with open(file_path, 'w') as file:
        json.dump(products, file, indent=4)

    return {"data": products[new_product.product_name]}


