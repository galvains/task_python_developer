#!/bin/sh

python db_api.py
gunicorn app:app --bind 0.0.0.0:5000