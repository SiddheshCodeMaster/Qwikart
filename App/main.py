from random import randrange
from datetime import datetime
import os
import json
from typing import Optional
import time

from . import schemas

from fastapi import FastAPI, Query, Request, Response, status,HTTPException, Depends 
from contextlib import asynccontextmanager
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import psycopg2
from psycopg2.extras import RealDictCursor

from . import models
from .database import engine,get_db

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

# # -----------------------------
# # Load products JSON once at startup
# # -----------------------------
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Startup: Load products
#     file_path = 'dataset/items.json'
#     try:
#         with open(file_path, 'r') as file:
#             app.state.products = json.load(file)
#     except (FileNotFoundError, json.JSONDecodeError):
#         app.state.products = {}
#     yield 

# -----------------------------
# Static & Template Setup
# -----------------------------

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# -----------------------------
# Product Endpoints (User)
# -----------------------------

@app.get("/Products", response_model= list[schemas.GetProduct])
def get_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products

@app.get("/Products/{id}", response_model= schemas.GetProduct)
def get_product(id: int, db: Session = Depends(get_db)):
    get_product = db.query(models.Product).filter(models.Product.id == id).first()
    if not get_product:
        raise HTTPException(status_code=404, detail=f"Product with ID {id} not found.")
    else:
        return get_product

# -----------------------------
# Product Endpoints (Admin)
# -----------------------------

@app.post("/Products", status_code=status.HTTP_201_CREATED, response_model= schemas.GetProduct)
def create_products(new_product: schemas.CreateProduct, db: Session = Depends(get_db)):
    
    create_product = models.Product(**new_product.dict())
    db.add(create_product)
    db.commit()
    db.refresh(create_product)
    return create_product

@app.put("/Products/{id}", status_code=status.HTTP_200_OK)
def update_product(id: int, updated_product: schemas.UpdateProduct,  db: Session = Depends(get_db)):

    update_product = db.query(models.Product).filter(models.Product.id == id)

    if update_product.first() == None:
        raise HTTPException (status_code=404, detail=f"Product with ID {id} not found.")
    else:
        update_product.update(updated_product.dict(),synchronize_session = False)
        db.commit()

        return update_product.first()
        
@app.delete("/Products/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int, db: Session = Depends(get_db)):

    delete_product = db.query(models.Product).filter(models.Product.id == id)

    if delete_product.first() == None:
        raise HTTPException(status_code=404, detail=f'Product with ID {id} not found.')
    else:
        delete_product.delete(synchronize_session = False)
        db.commit()
        Response(status_code=status.HTTP_204_NO_CONTENT)
