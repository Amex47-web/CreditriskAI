#!/bin/bash
cd "$(dirname "$0")"

# Create venv if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    ./venv/bin/pip install -r requirements.txt
fi

echo "Starting Credit Risk System API..."
source venv/bin/activate
export PYTHONPATH=$PYTHONPATH:$(pwd)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
