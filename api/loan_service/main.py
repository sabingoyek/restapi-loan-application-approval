from fastapi import FastAPI
from .router import router as  loan_router

app = FastAPI()

app.include_router(loan_router)

