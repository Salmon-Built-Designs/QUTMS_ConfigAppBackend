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
import pickle

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

        # Get uploaded file
        uploadedFile = request.files["file"]
        # Get upload user entered data from the form
        metadata = request.form

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
                # Create new log container and store in memory (override previous)
                global log_cache
                log_cache = process_file(os.path.join(
                    app.config["UPLOAD_FOLDER"], filename), metadata)

                return {"id":log_cache.id}

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
    try:
        global log_cache
        if log_cache == None:
            abort(400, description="No active session.")


        msg_type = None
        request_post = request.get_json()

        if request_post != None:
            request_info = request_post.items()

            msg_type = []

            for key, value in request_info:
                if key == "type":
                    msg_type.append(value)

        msg_range = log_cache.request_msgs(msg_type)
        return jsonify([msg.__dict__ for msg in msg_range])
        
    except Exception as e:
            print("Failed to get filtered data. Check json request format.")
            print(e)
            print(traceback.format_exc())
            abort(400, description="Bad request.")

@app.route('/analysis', methods=["GET", "POST"])
def analysis_data():
    try:
        if request.is_json:
            request_post = request.get_json()
            request_info = request_post.items()

            msg_type = None
            msg_id = None

            for key, value in request_info:
                if key == "type":
                    msg_type = value
                if key == "id":
                    msg_id = value

            return log_cache.request_data(msg_type, msg_id)

    except Exception as e:
        print("Failed to get graph data. Check json request format.")
        print(e)
        print(traceback.format_exc())
        abort(400, description="Bad request.")  

# Return current session ID
@app.route('/session')
def current_session():

    query = Log.query.get(log_cache.id)
    log_info = log_info_to_json(query)

    return json.dumps(log_info.__dict__)

def log_info_to_json(row):
    class found_log(object):
        def __init__(self, id, description, driver, location, date_created, date_recorded):
            self.id = id
            self.description = description
            self.driver = driver
            self.location = location
            self.date_created = str(date_created)
            self.date_recorded = date_recorded

    return found_log(row.id, row.description, row.driver, row.location, row.date_created, row.date_recorded)


# Get list of available sessions/log IDs
@app.route('/history')
def get_sessions():
    query = Log.query.all()
    found_logs = []

    for row in query:
        found_logs.append(log_info_to_json(row))

    return json.dumps([log.__dict__ for log in found_logs])

# Set new session for given ID
@app.route('/new-session', methods=["GET", "POST"])
def new_session():
    try:
        if request.is_json:
            request_id = request.get_json()
            query = request_id["id"]

            if query != None:
                SAVE_VOLUME = os.environ.get('SAVE_VOLUME')
                log_path = fr'{SAVE_VOLUME}/{query}/'

                filehandler = open(log_path + fr'log_dump.pkl', 'rb')

                global log_cache
                log_cache = pickle.load(filehandler)

                return f"Log (ID:{log_cache.id}) has been successfully restored."
        #else:
            #abort(404)
        
    except Exception as e:
            print("Failed to restore session.")
            print(e)
            print(traceback.format_exc())
            abort(400, description="Bad request.")

    #return f"Log (ID:{request_id}) could not be found.", 404


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
