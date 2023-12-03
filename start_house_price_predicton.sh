#! /bin/bash

uvicorn api_v1.customer_solvability_check__manager:app  --port 8004 --reload
