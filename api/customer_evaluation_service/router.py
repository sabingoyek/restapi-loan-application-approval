from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
import schemas
import crud

router = APIRouter(tags=["Customer Evaluation"])


@router.get("/{customer_id}/", response_model=float)
def customer_evaluation_score(customer_id: int, db: Session = Depends(get_db)):
    """
    Returns customer evaluation score
    """
    db_customer = crud.get_customer(db, customer_id=customer_id)
    if not db_customer:
        raise HTTPException(
            status_code=404, detail=f"Customer  with id: {customer_id} not found")
    income = db_customer.monthly_income
    expense = db_customer.monthly_expense

    score = 0 if income == 0 else 1 - (expense / income)

    return score
