from flask import Flask, request, jsonify, render_template, abort, json
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS

from functools import partial, wraps

import os
import datetime
import time
from backend.config import Config

import re  # only need this if you are on Windows (Darwin / mac doesnt need this)

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
DUMP_FOLDER = "JSON_dumps"
ALLOWED_EXTENSIONS = {"cc"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from backend import routes

#app = cors(app, allow_origin="*")