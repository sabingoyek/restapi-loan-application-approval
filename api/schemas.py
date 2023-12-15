from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import datetime



class CustomerCreate(BaseModel):
    first_name: str
    last_name: str
    birth_date: datetime
    phone_number: str
    email: str
    address: str
    monthly_income: int
    monthly_expense: int
    password: str

class CustomerUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_date: Optional[datetime] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    monthly_income: Optional[int] = None
    monthly_expense: Optional[int] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

class Customer(CustomerCreate):
    id: int    
    balance: int
    enrollment_date: datetime
    is_active: bool


# Schemas for operations on house
class HouseCreate(BaseModel):
    ms_sub_class: int 
    ms_zoning: str
    lot_area: int
    lot_config: str
    bldg_type: str
    overall_cond: int
    year_built: int
    year_remod_add: int
    exterior_1st: str
    bsmt_fin_sf2: int
    total_bsmt_sf: int
    #number: int
    #street: str
    #city: str
    is_on_market: bool

class HouseUpdate(BaseModel):
    ms_sub_class: Optional[int] = None 
    ms_zoning: Optional[str] = None
    lot_area: Optional[int] = None
    lot_config: Optional[str] = None
    bldg_type: Optional[str] = None
    overall_cond: Optional[int] = None
    year_built: Optional[int] = None
    year_remod_add: Optional[int] = None
    exterior_1st: Optional[str] = None
    bsmt_fin_sf2: Optional[int] = None
    total_bsmt_sf: Optional[int] = None
    #number: Optional[int] = None
    #street: Optional[str] = None
    #city: Optional[str] = None
    is_on_market: Optional[bool] = None

class House(HouseCreate):
    id: int



class LoanRequestStatus(str, Enum):
    under_review="under-review"
    canceled="canceled"
    accepted="accepted"
    rejected="rejected"


# Schemas for operations on Loan Request

class LoanRequestCreate(BaseModel):
    amount: int
    duration: int
    house_id: int
    customer_id: int

class LoanRequestUpdate(BaseModel):
    amount: Optional[int] = None
    duration: Optional[int] = None
    status: Optional[LoanRequestStatus] = None
    House_id: Optional[int] = None

class LoanRequest(LoanRequestCreate):
    id: int
    created_at: datetime
    status: LoanRequestStatus
    #owner: Customer

# Schemas for operations on Loans

class LoanCreate(BaseModel):
    amount: int
    duration: int
    loan_request_id: int

class LoanUpdate(BaseModel):
    amount: Optional[int] = None
    duration: Optional[int] = None
    start_at: Optional[datetime] = None

class Loan(LoanCreate):
    id: int
    approved_at: datetime
    start_at: datetime


# Schemas for operations on reimbursment

class ReimbursmentCreate(BaseModel):
    amount: int
    
class ReimbursmentUpdate(BaseModel):
    amount: Optional[int] = None
    loan_id: Optional[int] = None

class Reimbursment(ReimbursmentCreate):
    id: int
    loan_id: int
    create_at: datetime