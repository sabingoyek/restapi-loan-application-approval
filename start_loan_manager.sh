#! /bin/bash

uvicorn api_v1.loan_manager:app  --port 8005 --reload
