from random import randrange
from typing import Optional
from fastapi import Body, FastAPI

from pydantic import BaseModel

# Reading the welcome page:
from fastapi.responses import HTMLResponse
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

# Endpoint to retrieve the product (on product id basis)
@app.get("/Products/{id}")
def get_product(id: int):
    """
    Retrieve a product by its ID from the dataset.

    Args:
        id (int): The ID of the product to retrieve.

    Returns:
        dict: A dictionary with the format {"product_detail": product}, or an error message if not found.
    """
    # Load the product data from the JSON file
    file_path = 'dataset/items.json'
    try:
        with open(file_path, 'r') as file:
            products = json.load(file)
        
        # Search for the product with the given ID
        for product_name, product_details in products.items():
            if product_details.get("id") == id:
                return {"product_detail": {product_name: product_details}}
        
        # Return an error message if the product is not found
        return {"error": f"Product with ID {id} not found."}
    
    except FileNotFoundError:
        return {"error": "Product dataset file not found."}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format in the product dataset."}

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


