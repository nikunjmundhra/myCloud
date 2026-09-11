from flask import render_template, request , send_file ,current_app,abort ,redirect ,url_for,session 
from app import app
from werkzeug.utils import secure_filename
import os
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

@app.route("/",methods =["GET","POST"])
def home():
    name = None
    if request.method =="POST":
        name=request.form["name"]
        print(name)
    return render_template("index.html",
                           title ="Home",
                           name=name)

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            session["user_id"] = user.id
            return f"Logged in as user {session['user_id']}"

        return "Invalid username or password"

    return render_template(
        "login.html",
        title="Login"
    )

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

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        password_hash = generate_password_hash(password)

        user = User(
            username=username,
            password_hash=password_hash
        )

        db.session.add(user)
        db.session.commit()

        return "User registered successfully"

    return render_template(
        "register.html",
        title="Register"
    )