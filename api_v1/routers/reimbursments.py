"""
This module handle the reimbursment made for loans
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    # prefix="/loans",
    tags=["Reimbusments"],
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}},
)


@router.post("/loans/{loan_id}/reimbursments/", response_model=schemas.Reimbursment)
def create_reimbursment_for_loan(loan_id: int,
                                 reimbursment: schemas.ReimbursmentCreate,
                                 db: Session = Depends(get_db)):
    """
    Save a reimbursment and return it 
    """
    # delegate to midleware the checking of existence of the associated loan
    # to keep services loosly coupled
    # TO-DO: CHeck if the amount already paid don't exceed allocated before save new
    return crud.create_reimbursment(db=db, loan_id=loan_id, reimbursment=reimbursment)


@router.get("/loans/{loan_id}/reimbursments/", response_model=list[schemas.Reimbursment])
def read_loan_reimbursments(loan_id: int, skip: int = 0, limit: int = 100,
                            db: Session = Depends(get_db)):
    """
    Read and returns all reimbursments made for a specific loan
    """
    loans = crud.get_reimbursments_by_loan_id(
        db=db, loan_id=loan_id, skip=skip, limit=limit)
    return loans


@router.get("/reimbursments/", response_model=list[schemas.Reimbursment])
def read_all_reimbursments(db: Session = Depends(get_db)):
    """
    Read and returns all reimbursments
    """
    return crud.get_reimbursments(db=db)


@router.get("/reimbursments/{reimbursment_id}/", response_model=schemas.Reimbursment)
def read_reimbursment(reimbursment_id: int, db: Session = Depends(get_db)):
    """
    Returns a specific reimbursment
    """
    db_reimbursment = crud.get_reimbursment(
        db=db, reimbursment_id=reimbursment_id)
    if db_reimbursment is None:
        raise HTTPException(status_code=404,
                            detail=f"Reimbursment with id {reimbursment_id} does not exist")
    return db_reimbursment


@router.put('/reimbursments/{reimbursment_id}/',
            response_model=schemas.Reimbursment)
def update_reimbursment(reimbursment_id: int,
                        reimbursment: schemas.ReimbursmentUpdate,
                        db: Session = Depends(get_db)):
    """
    Update a reimbursment
    """
    db_reimbursment = crud.get_reimbursment(
        db, reimbursment_id=reimbursment_id)
    if db_reimbursment is None:
        raise HTTPException(status_code=404,
                            detail=f"Reimbursment with id {reimbursment_id} does not exist")
    reimbursment_updated = crud.update_reimbursment(
        db, reimbursment_id=reimbursment_id, reimbursment=reimbursment)
    return reimbursment_updated


@router.delete('/reimbursments/{reimbursment_id}/', response_model=schemas.Reimbursment)
def delete_reimbursment(reimbursment_id: int, db: Session = Depends(get_db)):
    """
    Delete a reimbursment
    """
    db_reimbursment = crud.get_reimbursment(
        db, reimbursment_id=reimbursment_id)
    if db_reimbursment is None:
        raise HTTPException(status_code=404,
                            detail=f"Reimbursment with id {reimbursment_id} does not exist")
    return crud.delete_reimbursment(db, reimbursment_id)
