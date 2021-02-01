from quart import Quart, request, jsonify, render_template, json
from functools import partial, wraps
from werkzeug.utils import secure_filename
import os
from quart_cors import cors
import datetime
import time
from can_parser import *

app = Quart(__name__)

UPLOAD_FOLDER = "uploads"
DUMP_FOLDER = "JSON_dumps"
ALLOWED_EXTENSIONS = {"txt", "CC"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app = cors(app, allow_origin="*")


async def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# Display upload page at root
@app.route("/upload")
async def upload_file_page():
    return await render_template("upload.html")


# Retrieve the uploaded log file
@app.route("/upload", methods=["GET", "POST"])
async def upload_file():
    if request.method == "POST":
        # Check file exists
        if "file" not in (await request.files):
            return "file not in request files"

        uploadedFile = (await request.files)["file"]

        # Check file is valid
        if uploadedFile.filename == "":
            return "file name blank"

        # Save file
        if uploadedFile and allowed_file(uploadedFile.filename):

            current_time = datetime.datetime.now().strftime("%d-%m-%y_%X_")
            filename = current_time + secure_filename(uploadedFile.filename)

            if not os.path.exists(UPLOAD_FOLDER):
                os.mkdir(UPLOAD_FOLDER)

            uploadedFile.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

            # Send file to the CAN parser to be processed
            msg_data = process_file(os.path.join(app.config["UPLOAD_FOLDER"], filename))

            # Convert the message list to JSON
            msg_data_json = json.dumps(
                [msg.__dict__ for msg in msg_data], ensure_ascii=False, indent=4
            )

            if not os.path.exists(DUMP_FOLDER):
                os.mkdir(DUMP_FOLDER)

            msg_dump = open(f"{DUMP_FOLDER}/{current_time}_JSON.json", "w")
            msg_dump.write(msg_data_json)
            msg_dump.close

            return jsonify([msg.__dict__ for msg in msg_data])
            # return msg_data_json


# app.run()
app.run(host="0.0.0.0", port="5873")
