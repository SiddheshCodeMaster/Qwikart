from typing import List
import time

from . import schemas

from fastapi import FastAPI, Response, status,HTTPException, Depends 
from sqlalchemy.orm import Session

import psycopg2
from psycopg2.extras import RealDictCursor

from . import models, utils
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

# -----------------------------
# Static & Template Setup
# -----------------------------

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# -----------------------------
# Product Endpoints (User)
# -----------------------------

@app.get("/Products", response_model= List[schemas.GetProduct])
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

@app.post("/createUser", status_code=status.HTTP_201_CREATED, response_model= schemas.userOut)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    new_user = models.Users(**user.dict())
    
    # # Hasing the password --> user.password
    
    if len(new_user.password.encode('utf-8')) > 72:
        raise HTTPException(status_code=400, detail=f"Password cannot be greater than 16 characters")
    else:
        new_user.password = utils.hash_password(new_user.password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

@app.get("/getUser/{id}", response_model= schemas.userOut)
def get_user(id: int, db: Session = Depends(get_db)):
    fetched_user = db.query(models.Users).filter(models.Users.id == id).first()
    if not fetched_user:
        raise HTTPException(status_code=404, detail=f"User with ID {id} not found.")
    else:
        return fetched_user

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
