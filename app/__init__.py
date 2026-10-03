from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

app.config.from_object("config")
@app.errorhandler(413)
def file_too_large(error):
    return render_template("413.html"), 413

db = SQLAlchemy(app)

from app import routes