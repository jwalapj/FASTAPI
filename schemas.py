from pydantic import BaseModel
from typing import Optional


class ItemCreate(BaseModel):
    name : str
    description: Optional[str]
    price : float

class ItemResponse(ItemCreate):
    id :int
