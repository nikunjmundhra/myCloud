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
        if file.filename == "":
            return render_template(
                "upload.html",
             title="Upload")
                
        filename=secure_filename(file.filename)
        base,extension=os.path.splitext(filename)
        i=1
        path=f"uploads/{filename}"
        if os.path.exists(path):
            filename=f"{base} ({i}){extension}"
            path=f"uploads/{filename}"
            while os.path.exists(f"uploads/{base} ({i}){extension}"):
                i+=1
                filename=f"{base} ({i}){extension}"
                path=f"uploads/{base} ({i}){extension}"
        file.save(path)
        print(f"Saved file: {filename}")

    return render_template(
        "upload.html",
        title="upload"
    )

@app.route("/files")
def files():
    files=os.listdir("uploads")
    correctfiles=[]
    for file in files:
        if file==".gitkeep":
            continue
        correctfiles.append(file)
    return render_template(
            "files.html",
            files=correctfiles,
            title="My Files"
        )