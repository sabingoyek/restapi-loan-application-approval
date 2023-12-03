"""
This evaluate customer base on his monthly income and monthly expense and return a score not greater than 1
The customer is not solvable as far as his score from 1

Further we can integrate another variable in this scoring
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud
from ..database import get_db

router = APIRouter(
    # prefix="/loans",
    tags=["Customer Evaluation Score"],
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}},
)


@router.get("/customer_evaluation/{customer_id}/", response_model=float)
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
