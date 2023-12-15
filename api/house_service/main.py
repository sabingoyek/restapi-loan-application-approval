from fastapi import FastAPI
from .router import router as  house_router

app = FastAPI()

app.include_router(house_router)

