from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas import ItemCreate, ItemResponse
from database import get_db
import schemas, models

router = APIRouter(
    prefix='/items',
    tags=['Items']
)

@router.post("/", response_model=schemas.ItemResponse)
async def create_item(Items: ItemCreate,db : Session = Depends(get_db) ):
    print(Items)
    create_item = models.Item(**Items.dict())
    db.add(create_item)
    db.commit()
    db.refresh(create_item)
    return create_item


@router.get("/{id}", response_model=ItemResponse)
async def get_itembyid(id: int, db: Session = Depends(get_db)):
    get_item = db.query(models.Item).filter(models.Item.id ==id).first()
    if get_item == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"Item with ID {id} not found")
    return get_item


@router.put("/{id}", response_model=ItemResponse)
async def update_items(id : int, Items :ItemCreate ,db : Session= Depends(get_db)):
    get_item = db.query(models.Item).filter(models.Item.id ==id)
    required_item = get_item.first()
    if required_item == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"Item with ID {id} not found")
   
    get_item.update(Items.dict())
    db.commit()
    db.refresh(required_item)
    return required_item



@router.delete("/{id}")
async def delete_items(id : int, db : Session= Depends(get_db)):
    get_item = db.query(models.Item).filter(models.Item.id ==id).first()
    if get_item == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"Item with ID {id} not found")
    db.delete(get_item)
    db.commit()
    return {"status": f"Item wit{id} is deleted"}
