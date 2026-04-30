#!/usr/bin/env bash
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python scripts/prepare_dataset.py
python scripts/train_model.py
python run.py
