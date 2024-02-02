# Standard library imports

# Remote library imports
import os

from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

# Load environment variables
load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "SQLALCHEMY_DATABASE_URI", "sqlite:///app.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "bcrypt_secret_key")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "jwt_secret_key")
    app.json.compact = False

    CORS(app, resources={r"/api/*": {"origins": "*"}})
    return app


def init_extensions(app):
    # Define metadata, instantiate db
    metadata = MetaData(
        naming_convention={
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        }
    )
    # Initialize extensions
    db = SQLAlchemy(app, metadata=metadata)
    ma = Marshmallow(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)
    bcrypt = Bcrypt(app)
    api = Api(app)

    return db, ma, bcrypt, jwt, api
