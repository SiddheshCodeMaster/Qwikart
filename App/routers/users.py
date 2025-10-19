from fastapi import status,HTTPException, Depends, APIRouter 
from sqlalchemy.orm import Session

from App import models, oauth2, schemas, utils
from App.database import get_db

router = APIRouter(
    tags=["Users"]
)

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
def get_user(id: int, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    
    if not current_user:
        raise HTTPException(status_code=403, detail="Not Authorized to perform the action.")
    else:
        if current_user.is_admin == False:
            raise HTTPException(status_code=403, detail="Admin Privileges Required to perform the action.")
        else:
            fetched_user = db.query(models.Users).filter(models.Users.id == id).first()
            if not fetched_user:
                raise HTTPException(status_code=404, detail=f"User with ID {id} not found.")
            else:
                return fetched_user