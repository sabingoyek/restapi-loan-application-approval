from fastapi import FastAPI
from .router import router as  house_valuation_router

app = FastAPI()

app.include_router(house_valuation_router)

