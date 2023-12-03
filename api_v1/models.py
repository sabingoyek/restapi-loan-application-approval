from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base
from .schemas import LoanRequestStatus


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    address = Column(String, nullable=False)
    monthly_income = Column(Integer, default=0, nullable=False)
    monthly_expense = Column(Integer, default=0, nullable=False)
    balance = Column(Integer, default=0, nullable=False)
    enrollment_date = Column(TIMESTAMP(timezone=True),
                             server_default=text('now()'), nullable=False)
    password = Column(String, nullable=False)  # hashed password
    is_active = Column(Boolean, default=True, nullable=False)


class House(Base):
    __tablename__ = "houses"

    id = Column(Integer, primary_key=True, index=True)
    ms_sub_class = Column(Integer, nullable=False,
                          comment="Identifies the type of dwelling involved in the sale")
    ms_zoning = Column(String, nullable=False,
                       comment="Identifies the general zoning classification of the sale")
    lot_area = Column(Integer, nullable=False,
                      comment="Lot size in square feet")
    lot_config = Column(String, nullable=False,
                        comment="Configuration of the lot")
    bldg_type = Column(String, nullable=False, comment="Type of dwelling")
    overall_cond = Column(Integer, nullable=False,
                          comment="Rates the overall condition of the house")
    year_built = Column(Integer, nullable=False,
                        comment="Original construction year")
    year_remod_add = Column(
        Integer, nullable=False, comment="Remodel date (same as construction date if no remodeling or additions)")
    exterior_1st = Column(String, nullable=False,
                          comment="Exterior covering on house")
    bsmt_fin_sf2 = Column(Integer, nullable=False,
                          comment="Type 2 finished square feet")
    total_bsmt_sf = Column(Integer, nullable=False,
                           comment="Total square feet of basement area")
    sale_price = Column(Integer, nullable=False,
                        comment="Sale Price")
    is_on_market = Column(Boolean, default=True, nullable=False,
                          comment="True if the house is for sale and False otherwise")
    # UniqueConstraint("number", "street", "city")
    # sale_price = Column(String, nullable=False, comment="")


class LoanRequest(Base):
    __tablename__ = "loan_requests"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('now()'), nullable=False)
    # status = Column(LoanRequestStatus, default=LoanRequestStatus.under_review, nullable=False)
    status = Column(
        String, default=LoanRequestStatus.under_review, nullable=False)

    house_id = Column(Integer, ForeignKey("houses.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)


class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    approved_at = Column(TIMESTAMP(timezone=True),
                         server_default=text('now()'), nullable=False)
    start_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    loan_request_id = Column(Integer, ForeignKey(
        "loan_requests.id"), nullable=False)
    UniqueConstraint("loan_request_id")


class Reimbursment(Base):
    __tablename__ = "reimbursments"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, nullable=False)
    create_at = Column(TIMESTAMP(timezone=True),
                       server_default=text('now()'), nullable=False)
    loan_id = Column(Integer, ForeignKey("loans.id"), nullable=False)
