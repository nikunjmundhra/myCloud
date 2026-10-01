import os

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")

BASE_DIR = os.path.dirname(__file__)

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "mycloud.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False