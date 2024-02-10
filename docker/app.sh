#!/bin/bash

sleep 5

uvicorn production_tasks.main:app --host 0.0.0.0 --port 8000
