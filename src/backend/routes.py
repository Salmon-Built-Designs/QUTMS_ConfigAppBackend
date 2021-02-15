from backend import app, db, guard, DUMP_FOLDER, UPLOAD_FOLDER, ALLOWED_EXTENSIONS, log_cache
from flask import request, abort, jsonify
from backend.can_parser import *
from werkzeug.utils import secure_filename
import flask_praetorian
from flask_sqlalchemy import SQLAlchemy
from backend.models import User, Log
import datetime
import os
import json
import traceback

# This file details all the routing to the front end including http requests, uploads, logins, etc

# Check that the file has the required extension


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Make the filename windows compatible


def sanitize_windows(filename: str) -> str:
    return (
        filename.replace(":", "")
        .replace("?", "")
        .replace("/", "")
        .replace("\\", "")
        .replace("|", "")
        .replace('"', "")
        .replace("<", "")
        .replace(">", "")
        .replace("*", "")
    )

# Retrieve the uploaded log file


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # Check file exists
        if "file" not in request.files:
            abort(400, description="File not found")

        uploadedFile = request.files["file"]

        # Check file is valid
        if uploadedFile.filename == "":
            abort(400, description="Bad file name")

        # Save file
        if uploadedFile and allowed_file(uploadedFile.filename):

            current_time = datetime.datetime.now().strftime("%d-%m-%y_%X_")
            filename = current_time + secure_filename(uploadedFile.filename)

            # the lines below are only needed if you are on Windows
            filename = sanitize_windows(filename)

            if not os.path.exists(UPLOAD_FOLDER):
                os.mkdir(UPLOAD_FOLDER)

            print(filename)
            uploadedFile.save(os.path.join(
                app.config["UPLOAD_FOLDER"], filename))

            # Send file to the CAN parser to be processed
            try:
                msg_data = process_file(os.path.join(
                    app.config["UPLOAD_FOLDER"], filename))

                # Create new log container and store in memory (override previous)
                new_log = log_container(msg_data)
                log_cache = new_log

                return {"id":new_log.id}
            except Exception as e:
                print("File processing failed. See exception:")
                print(e)
                print(traceback.format_exc())
                abort(400, description="Bad file format.")
        else:
            print("Bad file.")
            abort(400, description="Bad file name.")

# Respond to a request for log data
@app.route('/pull', methods=["GET", "POST"])
def pull_data():
    if request.method == "POST":
        try:
            request_info = request.get_json()
            request_info = request_info.items()
            msg_type = []

            for key, value in request_info:
                if key == "type":
                    msg_type = value

            msg_range = log_cache.request_msgs(msg_type)
            
        except Exception as e:
                print("Failed to get filtered data. Check json request format.")
                print(e)
                print(traceback.format_exc())
                abort(400, description="Bad request.")

    return jsonify([msg.__dict__ for msg in msg_range])

# Return current session ID
@app.route('/session')
def current_session():
    if request.method == "POST":
        return {"id":log_cache.id}

# Get list of available sessions/log IDs
@app.route('/history')
def get_sessions():
    raise Exception("Still need to implement history")
    return {"id":log_cache.id}

# Set new session for given ID
@app.route('/', methods=["GET", "POST"])

@app.route('/login', methods=['POST'])
def login():
    req = request.get_json(force=True)
    username = req.get('username', None)
    password = req.get('password', None)
    user = guard.authenticate(username,password)
    ret = {'access_token': guard.encode_jwt_token(user)}
    return ret, 200

@app.route('/refresh', methods=['POST'])
def refresh():
    print("refresh request")
    old_token = request.get_data()
    new_token = guard.refresh_jwt_token(old_token)
    ret = {'access_token': new_token}
    return ret, 200

@app.route('/protected')
@flask_praetorian.auth_required
def protected():
    return f'protected endpoint (allowed user {flask_praetorian.current_user().username})'
