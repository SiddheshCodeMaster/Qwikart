from fastapi import status,HTTPException, Depends, APIRouter 
from sqlalchemy.orm import Session

from App import models, schemas, utils
from App.database import get_db

router = APIRouter()

# -----------------------------
# User Endpoints (End Users side, Admin)
# -----------------------------

@router.post("/createUser", status_code=status.HTTP_201_CREATED, response_model= schemas.userOut)
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

@router.get("/getUser/{id}", response_model= schemas.userOut)
def get_user(id: int, db: Session = Depends(get_db)):
    fetched_user = db.query(models.Users).filter(models.Users.id == id).first()
    if not fetched_user:
        raise HTTPException(status_code=404, detail=f"User with ID {id} not found.")
    else:
        return fetched_user