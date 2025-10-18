from typing import List
from fastapi import Response, status,HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from App import models, schemas, oauth2
from App.database import get_db

router = APIRouter(
    tags=["Products"]
)

# -----------------------------
# Product Endpoints (End Users)
# -----------------------------

@router.get("/Products", response_model= List[schemas.GetProduct])
def get_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products

@router.get("/Products/{id}", response_model= schemas.GetProduct)
def get_product(id: int, db: Session = Depends(get_db)):
    get_product = db.query(models.Product).filter(models.Product.id == id).first()
    if not get_product:
        raise HTTPException(status_code=404, detail=f"Product with ID {id} not found.")
    else:
        return get_product
    
# -----------------------------
# Product Endpoints (Admin)
# -----------------------------

@router.post("/Products", status_code=status.HTTP_201_CREATED, response_model= schemas.GetProduct)
def create_products(new_product: schemas.CreateProduct, db: Session = Depends(get_db),current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    
    if not current_user:
        raise HTTPException(status_code=403, detail="Not Authorized to perform the action.")
    else:
        create_product = models.Product(**new_product.dict())
        db.add(create_product)
        db.commit()
        db.refresh(create_product)
        return create_product

@router.put("/Products/{id}", status_code=status.HTTP_200_OK)
def update_product(id: int, updated_product: schemas.UpdateProduct,  db: Session = Depends(get_db)):

    update_product = db.query(models.Product).filter(models.Product.id == id)

    if update_product.first() == None:
        raise HTTPException (status_code=404, detail=f"Product with ID {id} not found.")
    else:
        update_product.update(updated_product.dict(),synchronize_session = False)
        db.commit()

        return update_product.first()
        
@router.delete("/Products/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int, db: Session = Depends(get_db)):

    delete_product = db.query(models.Product).filter(models.Product.id == id)

    if delete_product.first() == None:
        raise HTTPException(status_code=404, detail=f'Product with ID {id} not found.')
    else:
        delete_product.delete(synchronize_session = False)
        db.commit()
        Response(status_code=status.HTTP_204_NO_CONTENT)
