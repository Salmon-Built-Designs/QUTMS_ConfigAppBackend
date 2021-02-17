#!/bin/bash

# Migrate db to new model if there are changes
echo 
conda run --no-capture-output -n cfback flask db upgrade

# Start up the backend server
conda run --no-capture-output -n cfback flask run --host=0.0.0.0

# Setup gunicorn (to be implemented)
#gunicorn --chdir src main:app -w 2 --threads 2 -b 0.0.0.0:5873

