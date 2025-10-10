from .database import Base
from sqlalchemy import Column, Integer, String, Float, Boolean, TIMESTAMP,text
from datetime import datetime

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
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

    