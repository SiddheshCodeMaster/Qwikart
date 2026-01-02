from typing import List
from fastapi import Response, status,HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func, or_ 
import re

from App import models, schemas, oauth2
from App.database import get_db

router = APIRouter(
    tags=["Products"]
)

# -----------------------------
# Product Endpoints (End Users)
# -----------------------------

@router.get("/Products", response_model= List[schemas.GetProduct])
def get_products(db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    
    if not current_user:
        raise HTTPException(status_code=403, detail="Not Authorized to perform the action.")
    else:
        products = db.query(models.Product).all()
        return products

@router.get("/Products/{id}", response_model= schemas.GetProduct)
def get_product(id: int, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    
    if not current_user:
        raise HTTPException(status_code=403, detail="Not Authorized to perform the action.")
    else:   
        get_product = db.query(models.Product).filter(models.Product.id == id).first()
        if not get_product:
            raise HTTPException(status_code=404, detail=f"Product with ID {id} not found.")
        else:
            return get_product
        
@router.get("/Products/search/{name}", response_model= List[schemas.GetProduct])
def search_products_by_name(name: str, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    
    if not current_user:
        raise HTTPException(status_code=403, detail="Not Authorized to perform the action.")
    else:
        # Normalizing incoming name string
        raw = (name or "").strip()
        norm = re.sub(r'[^A-Za-z0-9]+', '', raw).lower()

        # Pattern for simple contains, case-insensitive match
        pattern = f"%{raw}%"

        # Normalized comparison via PostgreSQL reex replace to handle differences

        try:
            products = db.query(models.Product).filter(
                or_(
                    models.Product.name.ilike(pattern),
                    func.lower(func.regexp_replace(models.Product.name, '[^a-z0-9]', '', 'gi')).like(f"%{norm}%")
                )
            ).all()
        except Exception:
            products = db.query(models.Product).filter(models.Product.name.ilike(pattern)).all()
        return products
               
@router.get("/Products/category/{category}", response_model= List[schemas.GetProduct])
def get_products_by_category(category: str, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    
    if not current_user:
        raise HTTPException(status_code=403, detail="Not Authorized to perform the action.")
    else:
        # Normalizing incoming category string
        raw = (category or "").strip()
        norm = re.sub(r'[^A-Za-z0-9]+', '', raw).lower()

        # Pattern for simple startswith, case-insensitive match
        pattern = f"{raw}%"

        # Normalized comparison via PostgreSQL reex replace to handle differences
        # ex: "Men's" vs "Mens"

        try: 
            products = db.query(models.Product).filter(
                or_(
                    models.Product.category.ilike(pattern),
                    func.lower(func.regexp_replace(models.Product.category, '[^a-z0-9]', '', 'gi')).like(f"{norm}%")
                )
            ).all()
        except Exception:
            products = db.query(models.Product).filter(models.Product.category.ilike(pattern)).all()
        
        return products
    
@router.get("/Products/description/{description}", response_model= List[schemas.GetProduct])
def get_products_by_description(description: str, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    
    if not current_user:
        raise HTTPException(status_code=403, detail="Not Authorized to perform the action.")
    else:
        # Normalizing incoming description string
        raw = (description or "").strip()
        norm = re.sub(r'[^A-Za-z0-9]+', '', raw).lower()

        # Pattern for simple contains, case-insensitive match
        pattern = f"%{raw}%"

        # Normalized comparison via PostgreSQL regex replace to handle differences

        try:
            products = db.query(models.Product).filter(
                or_(
                    models.Product.description.ilike(pattern),
                    func.lower(func.regexp_replace(models.Product.description, '[^a-z0-9]', '', 'gi')).like(f"%{norm}%")
                )
            ).all()
        except Exception:
            products = db.query(models.Product).filter(models.Product.description.ilike(pattern)).all()
        return products  

@router.get("/Products/location/{location}", response_model= List[schemas.GetProduct])
def get_products_by_location(location: str, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    
    if not current_user:
        raise HTTPException(status_code=403, detail="Not Authorized to perform the action.")
    else:
        # Normalizing incoming location string
        raw = (location or "").strip()
        norm = re.sub(r'[^A-Za-z0-9]+', '', raw).lower()

        # Pattern for simple startswith, case-insensitive match
        pattern = f"{raw}%"

        # Normalized comparison via PostgreSQL regex replace to handle differences
        # ex: "New York" vs "NewYork"

        try: 
            products = db.query(models.Product).filter(
                or_(
                    models.Product.location.ilike(pattern),
                    func.lower(func.regexp_replace(models.Product.location, '[^a-z0-9]', '', 'gi')).like(f"{norm}%")
                )
            ).all()
        except Exception:
            products = db.query(models.Product).filter(models.Product.location.ilike(pattern)).all()
        
        return products

@router.get("/Products/price_range/{min_price}/{max_price}", response_model= List[schemas.GetProduct])
def get_products_by_price_range(min_price: float, max_price: float, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    
    if not current_user:
        raise HTTPException(status_code=403, detail="Not Authorized to perform the action.")
    else:
        products = db.query(models.Product).filter(models.Product.price >= min_price, models.Product.price <= max_price).all()
        return products  
    
# -----------------------------
# Product Endpoints (Admin)
# -----------------------------

@router.post("/Products", status_code=status.HTTP_201_CREATED, response_model= schemas.GetProduct)
def create_products(new_product: schemas.CreateProduct, db: Session = Depends(get_db),current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    
    if not current_user:
        raise HTTPException(status_code=403, detail="Not Authorized to perform the action.")
    else:
        create_product = models.Product(**new_product.dict(), supplier_id = current_user.id)
        db.add(create_product)
        db.commit()
        db.refresh(create_product)
        return create_product

@router.put("/Products/{id}", status_code=status.HTTP_200_OK)
def update_product(id: int, updated_product: schemas.UpdateProduct,  db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):

    if not current_user:
        raise HTTPException(status_code=403, detail="Not Authorized to perform the action.")
    else: 
        if current_user.is_admin == False:
            raise HTTPException(status_code=403, detail="Admin Privileges Required to perform the action.")
        else:
            update_product = db.query(models.Product).filter(models.Product.id == id, models.Product.supplier_id == current_user.id)

            if update_product.supplier_id != current_user.id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                    detail = "Not Authorized to perform requested action")

            if update_product.first() == None:
                raise HTTPException (status_code=404, detail=f"Product with ID {id} not found.")
            else:
                update_product.update(updated_product.dict(),synchronize_session = False)
                db.commit()
                return update_product.first()
            
@router.delete("/Products/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):

    if not current_user:
        raise HTTPException(status_code=403, detail="Not Authorized to perform the action.")
    else:
        if current_user.is_admin == False:
            raise HTTPException(status_code=403, detail="Admin Privileges Required to perform the action.")
        else:
            delete_product = db.query(models.Product).filter(models.Product.id == id)

            if delete_product.supplier_id != current_user.id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                    detail = "Not Authorized to perform requested action")

            if delete_product.first() == None:
                raise HTTPException(status_code=404, detail=f'Product with ID {id} not found.')
            else:
                delete_product.delete(synchronize_session = False)
                db.commit()
                return Response(status_code=status.HTTP_204_NO_CONTENT)