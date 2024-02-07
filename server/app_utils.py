# app_utils.py contains utility functions for the Flask app, including validation, database, and error handling.
import json
import logging
import os

from flask import make_response
from sqlalchemy.exc import IntegrityError


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


def to_dict(model_instance, convert_price_to_dollars=False):
    """
    Converts a SQLAlchemy model instance into a dictionary, with optional price conversion.

    Args:
        model_instance: The SQLAlchemy model instance to convert.
        convert_price_to_dollars (bool): If True, convert price fields from cents to dollars.

    Returns:
        A dictionary representation of the model instance.
    """
    data = model_instance.__dict__.copy()

    data.pop("_sa_instance_state", None)

    # Convert price from cents to dollars if applicable
    if convert_price_to_dollars and "price" in data:
        data["price"] = cents_to_dollar(data["price"])

    return data


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
