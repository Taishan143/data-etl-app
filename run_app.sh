#!/bin/bash

# set up virtual environment

echo "Starting Virtual Environent..."
python3 -m venv etl_venv
source etl_venv/bin/activate

# Install dependencies

echo "Installing packages..."
python3 -m pip install -r requirements.txt

# Run the app

echo "Running ETL Process..."
python3 -m data_etl_app.main kaggle-config.yaml

# deactivate the virtual environment
deactivate