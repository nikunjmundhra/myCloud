from flask import render_template, request , send_file ,current_app,abort ,redirect ,url_for
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
    files = [
        file for file in os.listdir(app.config["UPLOAD_FOLDER"])
        if file != ".gitkeep"
    ]

    selection_mode = request.args.get("mode") == "delete"

    return render_template(
        "files.html",
        files=files,
        selection_mode=selection_mode
    )
        

@app.route("/preview/<filename>")
def preview(filename):
    path = f'{current_app.config["UPLOAD_FOLDER"]}/{filename}'
    if os.path.exists(path):
        return send_file(path)
    else:
        abort(404)

@app.route("/download/<filename>")
def download(filename):
    path = f'{current_app.config["UPLOAD_FOLDER"]}/{filename}'
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    else:
        abort(404)

@app.route("/delete", methods=["POST"])
def delete_files():

    selected_files = request.form.getlist("selected_files")

    for filename in selected_files:

        file_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        if os.path.exists(file_path) and os.path.isfile(file_path):
            os.remove(file_path)

    return redirect(url_for("files"))