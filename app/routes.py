from flask import render_template, request , send_file ,current_app,abort ,redirect ,url_for,session 
from app import app
from functools import wraps
from werkzeug.utils import secure_filename
import os
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User, File

def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))

        return view(*args, **kwargs)

    return wrapped_view


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

@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "POST":
        file = request.files["file"]
        if file.filename == "":
            return render_template(
                "upload.html",
                title="Upload"
            )
        filename = secure_filename(file.filename)
        base, extension = os.path.splitext(filename)
        i = 1
        path = os.path.join(
            current_app.config["UPLOAD_FOLDER"],
            filename
        )
        while os.path.exists(path):
            filename = f"{base} ({i}){extension}"
            path = os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                filename
            )
            i += 1
        file.save(path)
        new_file = File(
            filename=filename,
            user_id=session["user_id"]
        )
        db.session.add(new_file)
        db.session.commit()

        print(f"Saved file: {filename}")

    return render_template(
        "upload.html",
        title="Upload"
    )

@app.route("/files")
@login_required
def files():

    user_files = File.query.filter_by(
        user_id=session["user_id"]
    ).all()

    correctfiles = []

    for file in user_files:
        correctfiles.append(file.filename)

    selection_mode = request.args.get("mode") == "delete"

    return render_template(
        "files.html",
        files=correctfiles,
        title="My Files",
        selection_mode=selection_mode
    )
        

@app.route("/preview/<filename>")
@login_required
def preview(filename):

    file_record = File.query.filter_by(
        filename=filename,
        user_id=session["user_id"]
    ).first()
    if not file_record:
        abort(404)
    path = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        filename
    )
    if os.path.exists(path) and os.path.isfile(path):
        return send_file(path)
    abort(404)

@app.route("/download/<filename>")
@login_required
def download(filename):

    file_record = File.query.filter_by(
        filename=filename,
        user_id=session["user_id"]
    ).first()

    if not file_record:
        abort(404)

    path = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        filename
    )

    if os.path.exists(path) and os.path.isfile(path):
        return send_file(path, as_attachment=True)

    abort(404)

@app.route("/delete", methods=["POST"])
@login_required
def delete_files():
    selected_files = request.form.getlist("selected_files")
    for filename in selected_files:
        filename = secure_filename(filename)
        file_record = File.query.filter_by(
            filename=filename,
            user_id=session["user_id"]
        ).first()
        if not file_record:
            continue
        file_path = os.path.join(
            current_app.config["UPLOAD_FOLDER"],
            filename
        )
        if os.path.exists(file_path) and os.path.isfile(file_path):
            os.remove(file_path)
        db.session.delete(file_record)
    db.session.commit()
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

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))