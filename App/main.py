from fastapi import FastAPI
from . import models
from .database import engine
from .routers import products, users, auth

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

