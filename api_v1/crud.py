from sqlalchemy.orm import Session
from fastapi import HTTPException, Response, status

from . import models, schemas


def get_customer(db: Session, customer_id: int):
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    #print(customer)
    return customer

def get_customer_by_email(db: Session, email: str):
    return db.query(models.Customer).filter(models.Customer.email == email).first()


def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Customer).offset(skip).limit(limit).all()


def create_customer(db: Session, customer: schemas.CustomerCreate):
    fake_hashed_password = customer.password + "notreallyhashed"
    db_customer = models.Customer(**customer.model_dump())
    db_customer.hashed_password = fake_hashed_password
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def update_customer(db: Session, id: int, customer: schemas.CustomerCreate):
    db_customer = db.query(models.Customer).filter(models.Customer.id == id).first()
    customer_data = customer.model_dump(exclude_unset=True)
    #print(customer_data)
    for key, value in customer_data.items():
        setattr(db_customer, key, value)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def get_house(db: Session, house_id: int):
    house = db.query(models.House).filter(models.House.id == house_id).first()
    #print(house)
    return house


def get_house_price(db: Session, house_id: int):
    house = db.query(models.House).filter(models.House.id == house_id).first()
    return house.sale_price

#def get_house_by_address(db: Session, number: str, street: str, city: str):
#    return db.query(models.House).filter(models.House.number == number, models.House.street == street, models.House.city == city).first()


def get_houses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.House).offset(skip).limit(limit).all()


def create_house(db: Session, house: schemas.HouseCreate):
    db_house = models.House(**house.model_dump())
    db.add(db_house)
    db.commit()
    db.refresh(db_house)
    return db_house

def update_house(db: Session, id: int, house: schemas.HouseUpdate):
    db_house = db.query(models.House).filter(models.House.id == id).first()
    house_data = house.model_dump(exclude_unset=True)
    for key, value in house_data.items():
        setattr(db_house, key, value)
    db.add(db_house)
    db.commit()
    db.refresh(db_house)
    return db_house

def delete_house(db: Session, house_id: int):
    db_house_query = db.query(models.House).filter(models.House.id == house_id)
    db_house = db_house_query.first()
    if not db_house:
        raise HTTPException(status_code=404, 
                            detail=f"House with id {house_id} does not exist")
    db_house_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def get_loanrequest(db: Session, loanrequest_id: int):
    return db.query(models.LoanRequest).filter(models.LoanRequest.id == loanrequest_id).first()
    
def get_loanrequests(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.LoanRequest).offset(skip).limit(limit).all()


def create_loanrequest(db: Session, loanrequest: schemas.LoanRequestCreate):
    db_loanrequest = models.LoanRequest(**loanrequest.model_dump())
    try:
        db.add(db_loanrequest)
        db.commit()
        db.refresh(db_loanrequest)
        return db_loanrequest
    except:
        raise Exception()

def update_loanrequest(db: Session, id: int, loanrequest: schemas.LoanRequestUpdate):
    db_loanrequest = db.query(models.LoanRequest).filter(models.LoanRequest.id == id).first()
    loanrequest_data = loanrequest.model_dump(exclude_unset=True)
    for key, value in loanrequest_data.items():
        setattr(db_loanrequest, key, value)
    db.add(db_loanrequest)
    db.commit()
    db.refresh(db_loanrequest)
    return db_loanrequest


def get_loan(db: Session, loan_id: int):
    return db.query(models.Loan).filter(models.Loan.id == loan_id).first()

def get_loan_by_loan_request_id(db: Session, loan_request_id: int):
    return db.query(models.Loan).filter(models.Loan.loan_request_id == loan_request_id).first()
    
def get_loans(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Loan).offset(skip).limit(limit).all()

def create_loan(db: Session, loan: schemas.LoanCreate):
    """
    db_loan = models.Loan(**loan.model_dump())
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan
    """
    try:
        db_loan = models.Loan(**loan.model_dump())
        db.add(db_loan)
        db.commit()
        db.refresh(db_loan)
        return db_loan
    except:
        # check the appropriate error code for foreign key constraint violation
        raise HTTPException(status_code=500, 
                            detail=f"LoanRequest creation failed. Check details provided: {loan}")
    

def update_loan(db: Session, loan_id: int, loan: schemas.Loan):
    db_loan = db.query(models.Loan).filter(models.Loan.id == loan_id).first()
    loan_data = loan.model_dump(exclude_unset=True)
    for key, value in loan_data.items():
        setattr(db_loan, key, value)
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan


def get_reimbursment(db: Session, reimbursment_id: int):
    return db.query(models.Reimbursment).filter(models.Reimbursment.id == reimbursment_id).first()

def get_reimbursments_by_loan_id(db: Session, loan_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Reimbursment).filter(models.Reimbursment.loan_id == loan_id).all()
    
def get_reimbursments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Reimbursment).offset(skip).limit(limit).all()

def create_reimbursment(db: Session, loan_id: int, reimbursment: schemas.ReimbursmentCreate):
    """
    db_reimbursment = models.Reimbursment(**reimbursment.model_dump())
    db_reimbursment.loan_id = loan_id
    db.add(db_reimbursment)
    db.commit()
    db.refresh(db_reimbursment)
    return db_reimbursment
    """
    try:
        db_reimbursment = models.Reimbursment(**reimbursment.model_dump())
        db_reimbursment.loan_id = loan_id
        db.add(db_reimbursment)
        db.commit()
        db.refresh(db_reimbursment)
        return db_reimbursment
    except:
        # check the appropriate error code for foreign key constraint violation
        raise HTTPException(status_code=500, 
                            detail=f"Reimbursment creation failed. Check details provided: {reimbursment}")
    

def update_reimbursment(db: Session, reimbursment_id: int, reimbursment: schemas.ReimbursmentUpdate):
    db_reimbursment = db.query(models.Reimbursment).filter(models.Reimbursment.id == reimbursment_id).first()
    reimbursment_data = reimbursment.model_dump(exclude_unset=True)
    for key, value in reimbursment_data.items():
        setattr(db_reimbursment, key, value)
    db.add(db_reimbursment)
    db.commit()
    db.refresh(db_reimbursment)
    return db_reimbursment



def delete_reimbursment(db: Session, reimbursment_id: int):
    db_reimbursment_query = db.query(models.Reimbursment).filter(models.Reimbursment.id == reimbursment_id)
    db_reimbursment = db_reimbursment_query.first()
    if not db_reimbursment:
        raise HTTPException(status_code=404, 
                            detail=f"Reimbursment with id {reimbursment_id} does not exist")
    db_reimbursment_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


