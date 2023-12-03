# restapi-loan-application-approval
REST API for Loan Application Approval

The application is build by calling multiple API. 

The API are:
- Customer manager
- House manager
- Loan request manager
- Customer evaluaton manager
- House price prediction

All this API share the same database to maintain strong data consitency

To start the app:

- Start all of the above API by calling the scripts start_****.sh
The database will be initialized automatically
- You can load data in the house table by calling load_house_data.py code
- Then start the app by calling start_app.sh
