import Investigate
import os
from flask import Flask
from flask import Flask, render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import cv2

import string
import random

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = 'super secret key'.encode('utf8')

UPLOAD_FOLDER = os.path.join("static", "user_uploads", "original")
RESULT_FOLDER = os.path.join("static", "user_uploads", "result")
ALLOWED_EXTENSIONS = {'dicom', 'tiff', 'png', 'jpg', 'jpeg'}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["RESULT_FOLDER"] = RESULT_FOLDER
curImg_dir = ""

# check if the file is in accepted format
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

"""
Main page -> choose files to upload
"""
@app.route('/')
def main_page():
    return render_template("index.html")

"""
Investigate uploaded image
"""
@app.route('/upload', methods = ["GET", "POST"])
def upload_page():
    if request.method == "POST":
        try:
            # first clear the past uploads
            clear_past_uploads()
            clear_past_results()

            # get uploaded file
            f = request.files["file_input"]
            upload_dir = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(f.filename))
            f.save(upload_dir)

            return render_template("investigate.html", image_backend = upload_dir)

        except Exception as e:
            return redirect("/")
    return redirect("/")

"""
Classify chosen patch
"""
@app.route("/classify", methods = ["POST" , "GET"])
def classify_patch():
    if request.method == "POST":
        try:
            x = int(request.form["form_x"])
            y = int(request.form["form_y"])
            file_name = os.listdir(app.config["UPLOAD_FOLDER"])[0] # the first and the only file

            upload_dir = os.path.join(app.config["UPLOAD_FOLDER"], file_name)
            img = Investigate.classify_patch(src = upload_dir, x = x, y = y) # classify patch and overwrite original image

            clear_past_results()
            result_name = name_generator()
            result_dir = os.path.join(app.config["RESULT_FOLDER"], result_name + ".png")
            cv2.imwrite(result_dir, img) # save overwritten image

            return render_template("investigate.html", image_backend = result_dir)
        except Exception as e:
            return (str(e))

    return "NOT A POST METHOD"

"""
Clear all past uploaded images
"""
def clear_past_uploads():
    for files in os.listdir(app.config["UPLOAD_FOLDER"]):
        os.remove(os.path.join(app.config["UPLOAD_FOLDER"], files))

"""
Clear all past output images
"""
def clear_past_results():
    for files in os.listdir(app.config["RESULT_FOLDER"]):
        os.remove(os.path.join(app.config["RESULT_FOLDER"], files))

"""
Randomly Generate a name to save files
"""
def name_generator():
    name = ""
    letters = string.ascii_letters

    for i in range(15):
        name += random.choice(letters)

    return name

"""
Show Gallery
"""
@app.route("/gallery")
def show_gallery():
    return render_template("gallery.html")

@app.route("/About")
def about():
    return "About us"


if(__name__ == "__main__"):
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)  
