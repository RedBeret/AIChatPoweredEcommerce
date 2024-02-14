# Standard library imports

# Remote library imports
import os

from dotenv import load_dotenv
from flask import Flask, render_template, send_from_directory
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from openai import OpenAI
from sqlalchemy import MetaData

from flask_session import Session

load_dotenv()


app = Flask(
    __name__,
    static_url_path="",
    static_folder="../client/build",
    template_folder="../client/build",
)


# @app.route("/images/<path:filename>")
# def custom_images(filename):
#     return send_from_directory("server/static/img", filename)


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")
openai_client = OpenAI(api_key=OPENAI_API_KEY)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "default_secret_key")
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
Session(app)

# app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URI", "sqlite:///app.db")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
# if os.environ.get("RENDER"):
#     app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")
# else:
#     app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False
CORS(app)
# Define metadata, instantiate db
metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)
db = SQLAlchemy(metadata=metadata)
ma = Marshmallow(app)
ma.init_app(app)


migrate = Migrate(app, db)
db.init_app(app)
bcrypt = Bcrypt(app)
app.openai_client = openai_client
# Instantiate REST API
api = Api(app)

# Instantiate CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})
