import os

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")

BASE_DIR = os.path.dirname(__file__)

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

DATABASE_PATH = os.environ.get(
    "DATABASE_PATH",
    os.path.join(BASE_DIR, "mycloud.db")
)

SQLALCHEMY_DATABASE_URI = "sqlite:///" + DATABASE_PATH
SQLALCHEMY_TRACK_MODIFICATIONS = False