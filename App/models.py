from .database import Base
from sqlalchemy import Column, Integer, String, Float, Boolean, TIMESTAMP,text, ForeignKey
from datetime import datetime

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    is_available = Column(Boolean, default=True, nullable = False)
    category = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), 
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), 
                        nullable=True, onupdate= text('now()'))
    location_name = Column(String, nullable=False)
    supplier_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False
    )

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    firstname = Column(String, nullable=False)
    username = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    password = Column(String, nullable=False)       
    user_created_at = Column(TIMESTAMP(timezone=True), 
                        nullable=False, server_default=text('now()'))
    user_updated_at = Column(TIMESTAMP(timezone=True), 
                        nullable=True, onupdate= text('now()')) 
    is_admin = Column(Boolean, default=False, nullable = False)
    location_name = Column(String, nullable=True)

    