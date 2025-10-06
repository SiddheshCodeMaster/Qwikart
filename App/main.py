from random import randrange
from datetime import datetime
import os
import json
from typing import Optional
import time

from fastapi import FastAPI, Query, Request, Response, status,HTTPException
from contextlib import asynccontextmanager
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, conint

import psycopg2
from psycopg2.extras import RealDictCursor

# -----------------------------
# Establishing Database Connection
# -----------------------------

while True:
    try: 
        conn = psycopg2.connect(
                host='localhost',
                database='qwikart-central-db',
                user='postgres',
                password='password123', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection established") 
        break  
    except Exception as err:
        print("Error connecting to database: ", err)
        time.sleep(5)

# -----------------------------
# Defining PostgreSQL BIGINT range
# -----------------------------

BigInt = conint(ge=-9223372036854775808, le=9223372036854775807)

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

# -----------------------------
# Define data models using Pydantic
# -----------------------------
class ProductInfo(BaseModel):
    Price: float
    Description: str
    Quantity: int
    is_available: bool
    category: str
    location_name: Optional[str] = None

class Product(BaseModel):
    product_name: str
    information: ProductInfo

class Users(BaseModel):
    id: Optional[int]
    username: str
    lastname: str
    email: str
    age: int
    gender: str
    password: str
    user_created_at: Optional[datetime] = None
    user_updated_at: Optional[datetime] = None

class Admin(BaseModel):
    id: Optional[int]
    admin_username: str
    admin_password: str

class Api_transactions(BaseModel):
    id: BigInt
    username: str
    req_string: str
    res_String: str
    status: str
    err_code: Optional[int] = None
    err_msg: Optional[str] = None
    api_hit_id: BigInt

class Fullfilled_orders(BaseModel):
    api_transaction_id: BigInt
    order_status: str
    order_fullfilled: bool   


class History_Orders(BaseModel):
    api_transaction_id: BigInt 
    order_status: str
    order_created_at: Optional[datetime] = None
    order_fulfillment_info: Fullfilled_orders

class Location_information(BaseModel):
    location: str
    city: str
    state: str
    pincode: str
    country: str

# -----------------------------
# Static & Template Setup
# -----------------------------
app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="dynamic/templates")
app.mount("/dynamic", StaticFiles(directory="dynamic"), name="dynamic")
# app.mount("/dynamic/product_images", StaticFiles(directory="product_images"), name="product_images")

# -----------------------------
# Page Endpoints
# -----------------------------
    
@app.get("/welcomeQwikart", response_class=HTMLResponse)
def root():
    file_path = os.path.join("dynamic/templates", "welcome.html")
    with open(file_path, "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

@app.get("/explore", response_class=HTMLResponse)
def explore():
    file_path = os.path.join("dynamic/templates", "explore.html")
    with open(file_path, "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

@app.get("/consultation-form", response_class=HTMLResponse)
async def consultation_form(request: Request):
    return templates.TemplateResponse("consultation-form.html", {"request": request})

# -----------------------------
# Consultation Form Submission
# -----------------------------
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
# Product Endpoints (User)
# -----------------------------
@app.get("/get_all_products")
def get_products():
    return {"product_data": app.state.products}

@app.get("/Products")
def get_products():
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    return products

@app.get("/Products/{id}")
def get_product(id: int):
    cursor.execute("SELECT * FROM products WHERE id = %s",(str(id),))
    product = cursor.fetchone()
    if product:
        return product
    else:
        return {"error": f"Product with ID {id} not found."}

# -----------------------------
# Product Endpoints (Admin)
# -----------------------------
@app.post("/Products", status_code=status.HTTP_201_CREATED)
def create_products(new_product: Product):
    cursor.execute("INSERT INTO PRODUCTS (name, price, description, quantity, category, is_available, location_name) " \
    "VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING *",
                   (new_product.product_name, 
                    new_product.information.Price, 
                    new_product.information.Description, 
                    new_product.information.Quantity, 
                    new_product.information.category, 
                    new_product.information.is_available,
                    new_product.information.location_name))
    product_data = cursor.fetchone()

    conn.commit() 
    return {"data": product_data}

@app.put("/Products/{id}", status_code=status.HTTP_200_OK)
def update_product(id: int, updated_product: Product):
    cursor.execute("UPDATE products SET name=%s, price=%s, description=%s, quantity=%s, category=%s, is_available=%s WHERE id=%s RETURNING *",
                   (updated_product.product_name,
                    updated_product.information.Price,
                    updated_product.information.Description,
                    updated_product.information.Quantity,
                    updated_product.information.category,
                    updated_product.information.is_available,
                    str(id)))
    
    updated_data = cursor.fetchone()
    conn.commit()
    if updated_data == None: 
        raise HTTPException(status_code=404, detail=f"Product with ID {id} not found.")
    return {"data": updated_data}

    # for product_name, product_details in app.state.products.items():
    #     if product_details.get("id") == id:
    #         updated_data = {
    #             "Price": updated_product.information.Price,
    #             "Description": updated_product.information.Description,
    #             "Quantity": updated_product.information.Quantity,
    #             "Category": updated_product.information.category,
    #             "is_available": updated_product.information.is_available,
    #             "id": id,
    #             "product_image_path": updated_product.information.product_image_path
    #         }
    #         app.state.products[product_name] = updated_data
    #         with open('dataset/items.json', 'w') as file:
    #             json.dump(app.state.products, file, indent=4)
    #         return {"data": updated_data}
    # return JSONResponse(
    #     status_code=status.HTTP_404_NOT_FOUND,
    #     content={"message": f"Product with ID {id} not found."}
    # )

@app.delete("/Products/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int):

    cursor.execute("DELETE FROM products WHERE id = %s RETURNING *", (str(id),))
    deleted_product = cursor.fetchone()

    conn.commit()

    if deleted_product == None: 
        raise HTTPException(status_code=404, detail=f"Product with ID {id} not found.")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
