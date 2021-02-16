#!/bin/bash

conda run --no-capture-output -n cfback

flask db upgrade

flask run --host=0.0.0.0

#gunicorn --chdir src main:app -w 2 --threads 2 -b 0.0.0.0:5873

