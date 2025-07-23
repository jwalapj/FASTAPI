from fastapi import FastAPI
import models
from database import engine
from routers import Items, User, auth

# from .routers import Items

app = FastAPI()

# Database connection 
models.Base.metadata.create_all(bind = engine)

# connecting the router modules 
app.include_router(Items.router)
app.include_router(User.router)
app.include_router(auth.router)

# @app.get("/")
# async def home_page():
#     return {"Status": "Just checking"}
