"""
This module predict the price of the house based on the house id. All other information about the house is already stored in the database
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    # prefix="/loans",
    tags=["House Price Prediction"],
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}},
)


@router.get("/predict_price/{house_id}/", response_model=int)
def predict_house_price(house_id: int, db: Session = Depends(get_db)):
    """
    Returns the predicted house price
    """
    db_house = crud.get_house(db, house_id=house_id)
    if not db_house:
        raise HTTPException(
            status_code=404, detail=f"House  with id: {house_id} not found")
    return crud.get_house_price(db=db, house_id=house_id)
