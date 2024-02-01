#!/usr/bin/env python3

# Standard library imports

# Local imports
from config import api, app, db
from dotenv import load_dotenv

# Remote library imports
from flask import (
    Flask,
    flash,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_bcrypt import Bcrypt
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_restful import Resource
from flask_sqlalchemy import SQLAlchemy
from helpers import validate_not_blank, validate_type
from marshmallow import Schema, fields, validate
from models import Category, Order, OrderDetail, Product, ProductCategory, User
from sqlalchemy.exc import IntegrityError

from server.utilities import configure_app

# Builds app, set attributes
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'app.db')}"
)
load_dotenv()
app.secret_key = os.environ.get("SECRET_KEY")


@app.route("/")
def index():
    return "<h1>ChatPoweredEcommerce</h1>"


if __name__ == "__main__":
    configure_app()
    app.run(port=5555, debug=True)
