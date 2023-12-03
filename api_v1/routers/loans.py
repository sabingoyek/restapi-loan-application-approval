from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas, models
from ..database import get_db

router = APIRouter(
    #prefix="/loans",
    tags=["Loans"],
    #dependencies=[Depends(get_token_header)],
    #responses={404: {"description": "Not found"}},
)


@router.post("/loans/", response_model=schemas.Loan)
def create_loan(loan: schemas.LoanCreate, db: Session = Depends(get_db)):
    # delegate to midleware the checking of existence of the associated loan_request
    # to keep services loosly coupled
    db_loan_request = crud.get_loan_by_loan_request_id(db, loan.loan_request_id)
    if db_loan_request:
        raise HTTPException(status_code=400, detail="Loan already allocated to this loan request")
    return crud.create_loan(db=db, loan=loan)
    

@router.get("/loans/", response_model=list[schemas.Loan])
def read_loans(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    loans = crud.get_loans(db=db, skip=skip, limit=limit)
    return loans
    
@router.get("/loans/{loan_id}", response_model=schemas.Loan)
def read_loan(loan_id: int, db: Session = Depends(get_db)):
    db_loan = crud.get_loan(db=db, loan_id=loan_id)
    if db_loan is None:
        raise HTTPException(status_code=404, 
                            detail=f"Loan with id {loan_id} does not exist")
    return db_loan

@router.put('/loans/{loan_id}/', response_model=schemas.Loan)
def update_loan(loan_id: int, loan: schemas.LoanUpdate, db: Session = Depends(get_db)):
    db_loan = crud.get_loan(db, loan_id=loan_id)
    if db_loan is None:
        raise HTTPException(status_code=404, 
                            detail=f"Loan with id {loan_id} does not exist")
    loan_updated = crud.update_loan(db, loan_id, loan)
    return loan_updated