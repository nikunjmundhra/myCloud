from flask import render_template, request, send_file, current_app, abort, redirect, url_for, session
from app import app
from functools import wraps
from werkzeug.utils import secure_filename
import os
import shutil
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from app import db
from app.models import User, File


def _format_bytes(value):
    """Return a compact, user-friendly representation of a byte count."""
    units = ("B", "KB", "MB", "GB", "TB", "PB")
    size = float(value)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.1f} {unit}" if unit != "B" else f"{int(size)} {unit}"
        size /= 1024


def _storage_summary():
    """Read the filesystem that backs uploads (the Docker uploads volume in production)."""
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_folder, exist_ok=True)
    usage = shutil.disk_usage(upload_folder)
    percent_used = round((usage.used / usage.total) * 100) if usage.total else 0

    return {
        "total": _format_bytes(usage.total),
        "used": _format_bytes(usage.used),
        "free": _format_bytes(usage.free),
        "percent_used": percent_used,
    }


@app.context_processor
def inject_global_template_data():
    """Make session and storage data available to every shared template."""
    username = session.get("username")
    # Sessions created before the username was stored still receive the shared
    # header. The lookup happens once because the value is then saved in session.
    if not username and session.get("user_id"):
        user = db.session.get(User, session["user_id"])
        if user:
            username = user.username
            session["username"] = username

    return {
        "current_username": username,
        "storage": _storage_summary(),
    }

def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))

        return view(*args, **kwargs)

    return wrapped_view


@app.route("/")
def home():
    recent_files = []
    if "user_id" in session:
        recent_files = File.query.filter_by(user_id=session["user_id"]).order_by(
            File.id.desc()
        ).limit(5).all()

    return render_template("index.html", title="Home", recent_files=recent_files)

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            session["user_id"] = user.id
            session["username"] = user.username
            return redirect(url_for("home"))

        return render_template("login.html", title="Login", error="Invalid username or password"), 401

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
        path = os.path.join(
            current_app.config["UPLOAD_FOLDER"],
            file.filename
        )

        if os.path.isfile(path):
            correctfiles.append(file.filename)
        else:
            db.session.delete(file)

    db.session.commit()

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
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            return render_template(
                "register.html",
                title="Register",
                error="Enter both a username and password.",
                submitted_username=username,
            ), 400

        existing_user = User.query.filter(
            func.lower(User.username) == username.casefold()
        ).first()
        if existing_user:
            return render_template(
                "register.html",
                title="Register",
                error="That username is already taken. Please choose another.",
                submitted_username=username,
            ), 409

        password_hash = generate_password_hash(password)
        user = User(
            username=username,
            password_hash=password_hash
        )

        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            # The existing unique database constraint remains the final guard
            # if simultaneous identical registration requests pass the check.
            db.session.rollback()
            return render_template(
                "register.html",
                title="Register",
                error="That username is already taken. Please choose another.",
                submitted_username=username,
            ), 409

        return redirect(url_for("login"))

    return render_template(
        "register.html",
        title="Register"
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))
