from fastapi import FastAPI

from customer_service.main import app as customer_service_app
from house_service.main import app as house_service_app
from loan_request_service.main import app as loan_request_app
from loan_service.main import app as loan_app
from house_valuation_service.main import app as house_valuation_app
from customer_evaluation_service.main import app as customer_evaluation_app
from reimbursment_service.main import app as reimbursment_app

import models
from database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/customers", customer_service_app, "Customer Service")
app.mount("/houses", house_service_app, "House Service")
app.mount("/loanrequests", loan_request_app, "Loan Request Service")
app.mount("/loans", loan_app, "Loan Service")
app.mount("/house_valuation", house_valuation_app, "House Valuation Service")
app.mount("/customer_evaluation", customer_evaluation_app,
          "Customer Evaluation Service")
app.mount("/reimbursments", reimbursment_app, "Reimbursment Service")
