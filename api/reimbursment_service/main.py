from fastapi import FastAPI
from .router import router as reimbursment_router

app = FastAPI()

app.include_router(reimbursment_router)
