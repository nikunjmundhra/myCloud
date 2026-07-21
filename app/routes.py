from flask import render_template, request
from app import app
from werkzeug.utils import secure_filename
import os

@app.route("/",methods =["GET","POST"])
def home():
    name = None
    if request.method =="POST":
        name=request.form["name"]
        print(name)
    return render_template("index.html",
                           title ="Home",
                           name=name)

@app.route("/login")
def login():
    return render_template("login.html",title ="Login")

@app.route("/upload" , methods =["GET","POST"])
def upload():
     
    if request.method=="POST":
        file = request.files["file"]
        filename=secure_filename(file.filename)
        file.save(f"uploads/{filename}")
        print(f"Saved file : {filename}")

    return render_template(
        "upload.html",
        title="upload"
    )