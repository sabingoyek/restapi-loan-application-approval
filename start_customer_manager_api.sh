#! /bin/bash

uvicorn api_v1.customer_manager:app  --port 8000 --reload
