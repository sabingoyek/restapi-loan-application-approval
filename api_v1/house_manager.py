from fastapi import FastAPI, Depends, HTTPException

from sqlalchemy.orm import Session

from . import models
from .database import engine, get_db
from .routers  import customers, houses, loan_requests, loans, reimbursments, house_price_prediction, customer_evaluation

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(customers.router)
app.include_router(houses.router)
app.include_router(loan_requests.router)
app.include_router(loans.router)
app.include_router(reimbursments.router)
app.include_router(house_price_prediction.router)
app.include_router(customer_evaluation.router)