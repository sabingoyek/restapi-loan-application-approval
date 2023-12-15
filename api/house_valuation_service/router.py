from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
import schemas
import crud

router = APIRouter(tags=["House valuation"])


@router.get("/{house_id}/", response_model=int)
def predict_house_price(house_id: int, db: Session = Depends(get_db)):
    """
    Returns the predicted house price
    """
    db_house = crud.get_house(db, house_id=house_id)
    if not db_house:
        raise HTTPException(
            status_code=404, detail=f"House  with id: {house_id} not found")
    return crud.get_house_price(db=db, house_id=house_id)
