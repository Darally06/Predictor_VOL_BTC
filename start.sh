#!/bin/bash

# Lanzar FastAPI en segundo plano
uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# Lanzar Streamlit
streamlit run app/ui.py --server.port 10000 --server.address 0.0.0.0
