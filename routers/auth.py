from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from database import get_db
import schemas, models
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import timedelta,timezone,datetime
from fastapi.security import OAuth2PasswordBearer
import jwt 
from jwt.exceptions import InvalidTokenError


router = APIRouter(
    prefix="/login",
    tags=["Auth"]
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        print("------inside try")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("-------------------payload",payload)
        user_id = payload.get("user_id")
        print(user_id)
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id = user_id )
        print("----done with verification")
    except InvalidTokenError:
        raise credentials_exception
    return token_data


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    print("------inside getcurrent token")
    return verify_access_token(token, credentials_exception)
    

@router.post("/")
def login(user_creidentials: schemas.UserCreate,db: Session= Depends(get_db)):
    print("----------------------entered login")
    user = db.query(models.User).filter(models.User.email == user_creidentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if user_creidentials.password != user.password:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= f"Invalid cridentials")
    
    access_token = create_access_token(data={"user_id": user.id})

    return {"access_token":access_token , "token_type": "bearer"}