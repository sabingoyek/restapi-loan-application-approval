# REST-based Web Services for automatic assessment and approval of Home Loan Request

## Description

The Real Estate Loan Application Evaluation Composite Web Service is designed to automate the real estate loan application evaluation process using specialized web services. It enables customers to submit home loan applications expressed in natural language. The service integrates business information extraction, application text, credit check, property appraisal and approval decision components to provide a complete and accurate evaluation of loan applications.

The application consist of two part:

1. The APIs
They implement the function involved in loan request evaluation. They are:

    - Customer service
    - House service
    - Loan request service
    - Loan service
    - Customer evaluaton service
    - House price prediction service

2. An app that implement the the approval process logic by composing the previous web service. 



## How to start the application ?

In sequence, start the APIs, then the app.

To start the APIs, go to api folder and execute the commande:

```./start_api.sh```

To start the app, go to the project folder and execute the commande:

```./start_app.sh```


## How to use the application ?

The current implementation don't use NLP to process the loan request. The loans requests are submitted in workdir/new_loan_request folder as plain text file and follow a strict format.

> Votre Identifiant: 1
> Montant: 1000
> Duree: 20
> Identifiant de la maison: 1

Depending on the result of the evaluation, the request result can be found one of the folders workdir/accepted or workdir/rejected