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


app = Flask(__name__, static_folder="./static", static_url_path="/static")

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URI", "sqlite:///app.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
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
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# Instantiate REST API
api = Api(app)

# Instantiate CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})
