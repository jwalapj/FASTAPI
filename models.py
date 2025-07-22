from database import Base
from sqlalchemy import Column, String, Float,Integer

class Item(Base):
    __tablename__ ="Items"

    id = Column(Integer, primary_key=True, nullable=False,autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)


class User(Base):
    __tablename__ ="User"

    id = Column(Integer, primary_key=True, nullable=False,autoincrement=True)
    email = Column(String,nullable=False,unique=True)
    password = Column(String, nullable=False)