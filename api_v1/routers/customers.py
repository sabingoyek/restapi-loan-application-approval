from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    #prefix="/loanrequests",
    tags=["Customers"],
    #dependencies=[Depends(get_token_header)],
    #responses={404: {"description": "Not found"}},
)

@router.post("/customers/", response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    db_customer = crud.get_customer_by_email(db, email=customer.email)
    if db_customer:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_customer(db=db, customer=customer)

@router.get("/customers/", response_model=list[schemas.Customer])
def read_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    customers = crud.get_customers(db, skip=skip, limit=limit)
    return customers

@router.get("/customers/{customer_id}", response_model=schemas.Customer)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = crud.get_customer(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, 
                            detail=f"Customer with id {customer_id} does not exist")
    return db_customer

@router.put('/customers/{customer_id}/', response_model=schemas.Customer)
def update_customer(customer_id: int, customer: schemas.CustomerUpdate, db: Session = Depends(get_db)):
    db_customer = crud.get_customer(db, customer_id=customer_id)

    if db_customer is None:
        raise HTTPException(status_code=404, 
                            detail=f"Customer with id {customer_id} does not exist")
    
    customer_updated = crud.update_customer(db, customer_id, customer)
    return customer_updated