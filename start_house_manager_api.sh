#! /bin/bash

uvicorn api_v1.house_manager:app  --port 8001 --reload
