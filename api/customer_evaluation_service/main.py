from fastapi import FastAPI
from .router import router as  customer_router

app = FastAPI()

app.include_router(customer_router)

