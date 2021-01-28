from quart import Quart, request, jsonify, render_template
from functools import partial, wraps
from werkzeug.utils import secure_filename
import os
import quart_cors
from can_parser import *

app = Quart(__name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"txt", "cc"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


async def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# Display upload page at root
@app.route("/")
async def upload_file_page():
    return await render_template("upload.html")


# Retrieve the uploaded log file
@app.route("/", methods=["GET", "POST"])
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
            filename = secure_filename(uploadedFile.filename)
            uploadedFile.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

            # Send file to the CAN parser to be processed
            process_file(os.path.join(app.config["UPLOAD_FOLDER"], filename))

            return "File uploaded & processed"


app.run()
# app.run(host="0.0.0.0", port="5873")
