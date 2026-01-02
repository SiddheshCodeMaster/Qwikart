from datetime import datetime
from typing import Optional
from pydantic import BaseModel,conint,EmailStr

# -----------------------------
# Define data models using Pydantic
# -----------------------------

# -----------------------------
# Defining PostgreSQL BIGINT range
# -----------------------------

BigInt = conint(ge=-9223372036854775808, le=9223372036854775807)

# -----------------------------
# For All Product Related Endpoints
# -----------------------------

class Product(BaseModel):
    name: str
    price: float
    description: str
    quantity: int
    is_available: bool
    category: str
    location_name: Optional[str] = None

class userOut(BaseModel):
    username: str
    email: EmailStr
    is_admin: bool
    location_name: str

    class Config:
        orm_mode = True

class GetProduct(BaseModel):
    name: str
    price: float
    description: str
    quantity: int   
    category: str
    owner: userOut

    class Config:
        orm_mode = True


class CreateProduct(BaseModel):
    name: str
    price: float
    description: str
    quantity: int
    is_available: bool
    category: str
    location_name: Optional[str] = None

class UpdateProduct(BaseModel):
    price: float
    description: str                
    quantity: int
    is_available: Optional[bool] 
    location_name: Optional[str] = None

# -----------------------------
# For All User Related Endpoints
# -----------------------------

class CreateUser(BaseModel):
    firstname: str
    username: str
    lastname: str
    email: EmailStr
    age: int
    gender: str
    password: str
    is_admin: Optional[bool] = False
    location_name: Optional[str] = None
    user_created_at: Optional[datetime] = None
    user_updated_at: Optional[datetime] = None        

# -----------------------------
# For Admin Endpoints
# -----------------------------

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

class UserLogin(BaseModel):
    username: str
    password: str
    email: EmailStr

# -----------------------------
# For All  Related Endpoints
# -----------------------------    

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
# For all Login related Endpoints
# -----------------------------    

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str
    id: int