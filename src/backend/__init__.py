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

def create_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.commit()

#if testing locally
if os.environ.get('DATABASE_URL') == "":
    create_db()



from backend import routes, models
