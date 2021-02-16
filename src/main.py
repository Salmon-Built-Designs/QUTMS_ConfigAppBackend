
#from flask import cli
from backend import app, db, guard, models
from backend.models import User

# - IMPORTANT -
# To run this app, run 'flask run' from the folder that contains src

# This is not needed because the backend is started with 'flask run'
app.run(host="0.0.0.0", port="5873")

# curl 0.0.0.0:5873/pull -d '{"type": "PDM_Heartbeat"}' -H 'Content-Type: application/json'
