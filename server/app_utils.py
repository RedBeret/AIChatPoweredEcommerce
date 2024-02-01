import os

from dotenv import load_dotenv
from flask import make_response
from sqlalchemy.exc import IntegrityError

from .config import app, db


# Validation Functions
def validate_not_blank(value, field_name):
    """
    Validates that a given value is not blank.

    Args:
    value: The value to check.
    field_name (str): The name of the field for error messages.

    Returns:
    The original value if valid.

    Raises:
    ValueError: If the value is blank or empty.
    """
    if not value:
        raise ValueError(f"The {field_name} must not be blank.")
    if isinstance(value, str) and value.isspace():
        raise ValueError(f"The {field_name} must not be empty or just whitespace.")
    return value


def validate_positive_number(value, field_name):
    """
    Validates that a given value is a positive number.

    Args:
    value: The numerical value to check.
    field_name (str): The name of the field for error messages.

    Returns:
    The original value if valid.

    Raises:
    ValueError: If the value is negative.
    """
    if value < 0:
        raise ValueError(f"The {field_name} must not be negative.")
    return value


# Category Management
def validate_type(value, field_name, expected_type):
    """
    Validates and converts a value to a specified type.

    Args:
    value: The value to convert and check.
    field_name (str): The name of the field for error messages.
    expected_type: The expected type to convert to.

    Returns:
    The value converted to the expected type.

    Raises:
    ValueError: If the value cannot be converted to the expected type.
    """
    if not isinstance(value, expected_type):
        try:
            value = expected_type(value)
        except (ValueError, TypeError):
            raise ValueError(
                f"The {field_name} must be of type {expected_type.__name__}."
            )
    return value


# Utility Functions
def dollar_to_cents(dollar_amount):
    """
    Converts a dollar amount to cents, handling floats and integers separately.

    Args:
    dollar_amount (float, int, or str): The dollar amount to convert.

    Returns:
    int: The amount in cents.

    Raises:
    ValueError: If the dollar amount is invalid.
    """
    try:
        # Check if the input is already an integer
        if isinstance(dollar_amount, int):
            return dollar_amount * 100
        # Convert to float for string or float inputs, then to int
        return int(float(dollar_amount) * 100)
    except ValueError:
        raise ValueError(f"Invalid dollar amount: {dollar_amount}")


def cents_to_dollar(cents):
    """
    Converts an integer representing cents to a string formatted as dollars.

    Args:
    cents (int): The amount in cents.

    Returns:
    str: The formatted dollar string.
    """
    return f"${cents / 100:.2f}"


def normalize_price_input(price_input):
    """
    Normalizes price input to be stored in the database as cents.

    Args:
    price_input: The price input, either as an integer, float, or string.

    Returns:
    int: The price converted to cents.

    Raises:
    ValueError: If the price input is invalid.
    """
    return dollar_to_cents(price_input)


def to_dict(self, convert_price_to_dollars=False):
    data = {
        "id": self.id,
        "name": self.name,
        "description": self.description,
        "price": self.price / 100 if convert_price_to_dollars else self.price,
        "item_quantity": self.item_quantity,
        "image_url": self.image_url,
        "imageAlt": self.imageAlt,
    }
    return data


# Session and Authentication Helpers
def authenticate_user(username, password):
    """
    Authenticates a user based on their username and password.

    Args:
    username (str): The username of the user.
    password (str): The password to be authenticated.

    Returns:
    User: The authenticated user object or None if authentication fails.
    """
    user = User.query.filter_by(username=username).first()

    if user and user.authenticate(password):
        return user
    return None


# Application configuration
# def configure_app():
#     """
#     Configures the Flask app with database settings and secret key.

#     Sets up the database URI and loads environment variables.
#     """
#     BASE_DIR = os.path.abspath(os.path.dirname(__file__))
#     DATABASE = os.environ.get(
#         "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'app.db')}"
#     )
#     load_dotenv()
#     app.secret_key = os.environ.get("SECRET_KEY")


# Database Utility Functions
def commit_session(session):
    """
    Commits a session and handles IntegrityError by rolling back.

    Args:
    session: The SQLAlchemy session to commit.

    If an IntegrityError occurs during commit, the session is rolled back,
    and the exception is re-raised.
    """
    try:
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise exc


# Error handling


def create_error_response(message, status_code):
    """
    Creates an error response with a given message and status code.

    Args:
    message (str): The error message.
    status_code (int): The HTTP status code for the response.

    Returns:
    dict: The error response in the form of a dictionary.
    """
    return make_response({"error": message}, status_code)


def get_or_create_category(category_name):
    """
    Retrieves or creates a category with the given name.

    Args:
    category_name (str): The name of the category to retrieve or create.

    Returns:
    Category: The category object.

    Creates a new category with the given name if it doesn't exist.
    """
    category = db.session.query(Category).filter_by(name=category_name).first()
    if category is None:
        category = Category(name=category_name)
        db.session.add(category)
        commit_session(db.session)
    return category
