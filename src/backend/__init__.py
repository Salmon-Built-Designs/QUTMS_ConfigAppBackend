from flask import Flask, request, jsonify, render_template, abort, json
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS
import flask_praetorian
from functools import partial, wraps

import os
import datetime
import time
from backend.config import Config

import re  # only need this if you are on Windows (Darwin / mac doesnt need this)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

UPLOAD_FOLDER = "uploads"
DUMP_FOLDER = "JSON_dumps"
ALLOWED_EXTENSIONS = {"cc"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


db = SQLAlchemy()
guard = flask_praetorian.Praetorian()
migrate = Migrate(app, db)


from backend.models import User
guard.init_app(app, User)

# Does running init erase previous db?
db.init_app(app)

# Create container for log data
global log_cache
log_cache = None

# def create_db():
#     with app.app_context():
#         #db.drop_all()
#         db.create_all()
#         db.session.commit()

# if (os.environ.get('DOCKER_ENV') == True):
#     print(f"{bcolors.WARNING}Docker environment detected{bcolors.ENDC}")
# else:
#     print(f"{bcolors.WARNING}###############################{bcolors.ENDC}")
#     print(f"{bcolors.WARNING}Local dev environment detected.{bcolors.ENDC}")
#     print(f"{bcolors.WARNING}###############################{bcolors.ENDC}")

# create_db()


from backend import routes, models
