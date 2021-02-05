from backend import app, db, DUMP_FOLDER, UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from flask import request, abort, jsonify
from backend.can_parser import *
from werkzeug.utils import secure_filename
import datetime
import os

# This file details all the routing to the front end including http requests, uploads, logins, etc

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


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
            uploadedFile.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

            # Send file to the CAN parser to be processed
            try:

                msg_data = process_file(os.path.join(app.config["UPLOAD_FOLDER"], filename))

                # Convert the message list to JSON
                msg_data_json = json.dumps(
                    [msg.__dict__ for msg in msg_data], ensure_ascii=False, indent=4
                )

                if not os.path.exists(DUMP_FOLDER):
                    os.mkdir(DUMP_FOLDER)

                msg_dump = open(
                    f"{DUMP_FOLDER}/" + sanitize_windows(f"{current_time}_JSON.json"), "w"
                )
                msg_dump.write(msg_data_json)
                msg_dump.close

                return jsonify([msg.__dict__ for msg in msg_data])
            except:
                print("Bad format. Please upload a valid binary CC file.")
                abort(400, description="Bad file format.")
        else:
            print("Bad file.")
            abort(400, description="Bad file name.")
