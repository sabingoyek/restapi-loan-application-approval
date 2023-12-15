from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
import schemas
import crud

router = APIRouter(tags=["Houses"])


@router.post("/", response_model=schemas.House)
def create_house_(house: schemas.HouseCreate, db: Session = Depends(get_db)):
    # db_house = crud.get_house_by_address(db, number=house.number, street=house.street, city=house.city)
    # if db_house:
    #    raise HTTPException(status_code=400, detail="House already registered.")
    return crud.create_house(db=db, house=house)


@router.get("/", response_model=list[schemas.House])
def read_houses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    houses = crud.get_houses(db, skip=skip, limit=limit)
    return houses


@router.get("/{house_id}", response_model=schemas.House)
def read_house(house_id: int, db: Session = Depends(get_db)):
    db_house = crud.get_house(db, house_id=house_id)
    if db_house is None:
        raise HTTPException(status_code=404,
                            detail=f"House with id {house_id} does not exist")
    return db_house


@router.put('/{house_id}/', response_model=schemas.House)
def update_house(house_id: int, house: schemas.HouseUpdate, db: Session = Depends(get_db)):
    db_house = crud.get_house(db, house_id=house_id)
    if db_house is None:
        raise HTTPException(status_code=404,
                            detail=f"House with id {house_id} does not exist")
    house_updated = crud.update_house(db, house_id, house)
    return house_updated


@router.delete('/{house_id}/', status_code=status.HTTP_204_NO_CONTENT)
def delete_house(house_id: int, db: Session = Depends(get_db)):
    db_house = crud.get_house(db, house_id=house_id)
    if db_house is None:
        raise HTTPException(status_code=404,
                            detail=f"House with id {house_id} does not exist")
    return crud.delete_house(db, house_id=house_id)
