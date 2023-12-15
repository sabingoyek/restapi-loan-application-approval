from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
import schemas, models
import crud

router = APIRouter(tags=["Loan Requests"])


@router.post("/", response_model=schemas.LoanRequest)
def create_loanrequest(loanrequest: schemas.LoanRequestCreate, db: Session = Depends(get_db)):
    # delegate to midleware the checking of existence of the customer and the house
    # to keep services loosly coupled
    try:
        db_loanrequest = models.LoanRequest(**loanrequest.model_dump())
        db.add(db_loanrequest)
        db.commit()
        db.refresh(db_loanrequest)
        return db_loanrequest
    except:
        # check the appropriate error code for foreign key constraint violation
        raise HTTPException(status_code=500,
                            detail=f"LoanRequest creation failed. Check details provided: {loanrequest}")


@router.get("/", response_model=list[schemas.LoanRequest])
def read_loanrequests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    loanrequests = crud.get_loanrequests(db, skip=skip, limit=limit)
    return loanrequests


@router.get("/{loanrequest_id}", response_model=schemas.LoanRequest)
def read_loanrequest(loanrequest_id: int, db: Session = Depends(get_db)):
    db_loanrequest = crud.get_loanrequest(db, loanrequest_id=loanrequest_id)
    if db_loanrequest is None:
        raise HTTPException(status_code=404,
                            detail=f"LoanRequest with id {loanrequest_id} does not exist")
    return db_loanrequest


@router.put('/{loanrequest_id}/', response_model=schemas.LoanRequest)
def update_loanrequest(loanrequest_id: int, loanrequest: schemas.LoanRequestUpdate, db: Session = Depends(get_db)):
    db_loanrequest = crud.get_loanrequest(db, loanrequest_id=loanrequest_id)
    if db_loanrequest is None:
        raise HTTPException(status_code=404,
                            detail=f"LoanRequest with id {loanrequest_id} does not exist")

    loanrequest_updated = crud.update_loanrequest(
        db, loanrequest_id, loanrequest)
    return loanrequest_updated
