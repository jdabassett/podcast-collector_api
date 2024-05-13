from fastapi import FastAPI

from .database import Base, engine
from .routers.user_router import router as user_router
from .routers.authenication_router import router as authentication_router

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(authentication_router)
app.include_router(user_router)