from backend import app, db, guard, models
from backend.models import User, Log

# - IMPORTANT -
# To run this app, use 'flask run'

# To start interactive shell to access db commands, while the container is running use:
# $ docker exec -ti cfh_backend /bin/bash

# Activate the conda environment cfback to access flask
# $ conda activate cfback

# Use commands, e.g. $ flask create-db

@app.cli.command("create-db")
def create_new_db():
    with app.app_context():
        db.create_all()
        db.session.commit()
        print("Database created successfully.")

@app.cli.command("clear-db")
def delete_db():
    if input("WARNING THIS WILL ERASE THE LOG DATABASE. ARE YOU SURE YOU WANT TO PROCEED?(y/n)") == "y":
        with app.app_context():
            db.drop_all()
            db.session.commit()
            print("Database cleared successfully.")

@app.cli.command("list-logs")
def get_logs():
    query = Log.query.all()
    print(query)


# This is not needed because the backend is started with 'flask run'
# Uncomment this to use VSC debugger
#app.run(host="0.0.0.0", port="5873")

# curl 0.0.0.0:5873/pull -d '{"type": "PDM_Heartbeat"}' -H 'Content-Type: application/json'
# curl 0.0.0.0:5873/upload -F "file=@LOG.CC"
# curl 0.0.0.0:5873/analysis -d '{"type": "BMS_TransmitVoltage"}' -H 'Content-Type: application/json'
# curl 0.0.0.0:5873/history
