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

# Pydantic BaseModel for new product data
class Product(BaseModel):
    product_name: str
    information: ProductInfo

# Mount the static folder for serving static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/welcomeQwikart", response_class=HTMLResponse)
def root():
     # Get the path of the HTML file
    file_path = os.path.join("templates", "welcome.html")
    
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

# Endpoint to create new products
@app.post("/createProducts")
def create_products(new_product: Product):    
    # Process the incoming data to store in the required structure
    return {
        "added_products": {
            new_product.product_name: {
                "Price": new_product.information.Price,
                "Description": new_product.information.Description,
                "Quantity": new_product.information.Quantity
            }
        }
    }

