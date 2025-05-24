#!/bin/bash

# set up virtual environment

python3 -m venv etl_venv
source etl_venv/bin/activate

# Install dependencies

python3 -m pip install -r requirements.txt

# Run the app

python3 -m data_etl_app/main.py kaggle-config.yaml