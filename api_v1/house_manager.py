from fastapi import FastAPI, Depends, HTTPException

from sqlalchemy.orm import Session

from . import models
from .database import engine, get_db
from .routers import houses

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(houses.router)
