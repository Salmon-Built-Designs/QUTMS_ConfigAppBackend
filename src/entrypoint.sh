#!/bin/bash

# Migrate db to new model if there are changes
echo Migrating database changes if there are any...
conda run --no-capture-output -n cfback flask db upgrade &> /dev/null
echo Database migration completed.

# Start up the backend server
echo Starting up backend server...
conda run --no-capture-output -n cfback flask run --host=0.0.0.0

# Setup gunicorn (to be implemented)
#gunicorn --chdir src main:app -w 2 --threads 2 -b 0.0.0.0:5873

