import os

from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

db = SQLAlchemy(app)

SECRET_KEY = "secret-key"

root_dir: str = os.path.dirname(os.path.abspath(__file__))
database = "sqlite:///" + os.path.join(root_dir, "db.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = database
