from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from database import get_db
import schemas, models

router = APIRouter(
    prefix="/user",
    tags=["User"]
)



@router.post("/", response_model= schemas.UserCreateOut)
def create_user(user: schemas.UserCreate ,db: Session = Depends(get_db)):
    # hass the password 
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user