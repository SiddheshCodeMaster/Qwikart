import time
from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor

from . import models
from .database import engine

from .routers import products, users, auth

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

#-----------------------------
# Setting API Routers
#-----------------------------

app.include_router(products.router)
app.include_router(users.router)
app.include_router(auth.router)

