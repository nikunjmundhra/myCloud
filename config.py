import os

SECRET_KEY = "my_secret_key"

BASE_DIR = os.path.dirname(__file__)

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "mycloud.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False