#!/bin/bash

sleep 5

cd production_tasks || exit

uvicorn main:app --host 0.0.0.0 --port 8000
