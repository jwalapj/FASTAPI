from pydantic import BaseModel
from typing import Optional


class ItemCreate(BaseModel):
    name : str
    description: Optional[str]
    price : float

class ItemResponse(ItemCreate):
    id :int


class UserCreate(BaseModel):
    email:str
    password:str


class UserCreateOut(BaseModel):
    email: str
    id: int

class TokenData(BaseModel):
    id:Optional[int] =None
