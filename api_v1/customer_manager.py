from fastapi import FastAPI, Depends

from . import models
from .database import engine, get_db
from .routers import customers

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(customers.router)
