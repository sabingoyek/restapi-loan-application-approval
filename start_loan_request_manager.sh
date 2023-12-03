#! /bin/bash

uvicorn api_v1.loan_request_manager:app  --port 8002 --reload
