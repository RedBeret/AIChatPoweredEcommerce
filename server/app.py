#!/usr/bin/env python3
"""
Main application file for AiChatPoweredEcommerce.
Sets up the Flask application, API resources, and routes. Handles user authentication,
product management, shipping information, and chat functionality.
"""
import openai
from click import prompt
from dotenv import load_dotenv
from flask_migrate import current
from pydantic import conset

load_dotenv()
import logging
import os

import bcrypt
from flask import Flask, render_template, send_from_directory
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
import traceback
from datetime import datetime
from pathlib import Path

from config import api, app, db, ma, openai_client
from flask import jsonify, make_response, request, session
from flask_bcrypt import Bcrypt
from flask_marshmallow import fields
from flask_restful import Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, ValidationError, fields, validate
from models import (
    ChatMessage,
    Color,
    Order,
    OrderDetail,
    Product,
    ShippingInfo,
    UserAuth,
    UserSession,
    db,
)
from openai import OpenAI
from sqlalchemy.dialects import postgresql
from sqlalchemy.exc import IntegrityError

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DATABASE_URI", f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'app.db')}"
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
DATABASE_URI = os.getenv("DATABASE_URI")

app.config.update(
    SECRET_KEY=SECRET_KEY,
    SESSION_TYPE="filesystem",
    SQLALCHEMY_DATABASE_URI=DATABASE_URI,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

bcrypt = Bcrypt(app)
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

script_dir = Path(__file__).parent
file_path = script_dir / "data" / "support_guide.txt"


@app.route("/")
def index():
    return render_template("index.html")


@app.errorhandler(404)
def not_found(e):
    return render_template("index.html")


# User Authentication Resources
# ------------------------------


class UserAuthSchema(ma.SQLAlchemyAutoSchema):
    """
    Marshmallow schema for serializing and deserializing UserAuth instances.
    Facilitates user input validation upon registration and formats output for API responses.
    Excludes the password_hash field from serialization for security.
    """

    class Meta:
        model = UserAuth
        load_instance = True
        exclude = ("password_hash",)  # Excludes sensitive information from the output.

    # Ensures passwords are at least 6 characters long, enhancing basic security.
    password = fields.Str(
        load_only=True, required=True, validate=validate.Length(min=6)
    )


class UserAuthResource(Resource):
    """
    RESTful resource for managing UserAuth entities, supporting operations like retrieval, creation, and deletion of user accounts.
    """

    def get(self):
        """Fetches and returns all user accounts, excluding sensitive password hashes."""
        users = UserAuth.query.all()
        user_schema = UserAuthSchema(many=True, only=["id", "username", "email"])
        return make_response(jsonify(user_schema.dump(users)), 200)

    def post(self):
        """Creates a new user account with provided username, email, and password."""
        user_data = request.get_json()

        if not user_data:
            return make_response(jsonify({"error": "No input data provided"}), 400)

        username = user_data.get("username").lower()
        email = user_data.get("email")
        password = user_data.get("password")

        if not all([username, email, password]):
            return make_response(
                jsonify({"error": "Missing username, email, or password"}), 400
            )

        if len(password) < 6:
            return make_response(
                jsonify({"error": "Password must be at least 6 characters long"}), 400
            )

        if UserAuth.query.filter_by(username=username).first():
            return make_response(jsonify({"error": "Username already exists"}), 409)

        if UserAuth.query.filter_by(email=email).first():
            return make_response(jsonify({"error": "Email already exists"}), 409)

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        new_user = UserAuth(
            username=username, email=email, password_hash=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()

        new_user_session = UserSession(
            user_id=new_user.id, started_at=datetime.utcnow()
        )
        db.session.add(new_user_session)
        db.session.commit()

        session["user_id"] = new_user.id
        session["username"] = new_user.username
        session["logged_in"] = True
        session["session_id"] = new_user_session.id

        return make_response(
            jsonify(
                {
                    "message": "User created successfully and logged in",
                    "id": new_user.id,
                    "username": new_user.username,
                    "email": new_user.email,
                    "session_id": new_user_session.id,
                }
            ),
            201,
        )

    def delete(self):
        """Deletes a user account after verifying provided credentials."""
        try:
            data = request.get_json()
            if not all(key in data for key in ("username", "password")):
                return make_response(
                    {"error": "Username and password are required"}, 400
                )

            username = data["username"].lower()
            password = data["password"]

            user = UserAuth.query.filter_by(username=username).first()

            if user and bcrypt.check_password_hash(user.password_hash, password):
                db.session.delete(user)
                db.session.commit()
                session.clear()
                return make_response({"message": "User deleted successfully"}, 200)
            elif user:
                return make_response({"error": "Incorrect password"}, 401)
            else:
                return make_response({"error": "User not found"}, 404)
        except Exception as error:
            return make_response({"error": str(error)}, 500)

    def patch(self):
        """Updates a user's password after verifying the current password."""
        data = request.get_json()
        username = data["username"].lower()
        user = UserAuth.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password_hash, data["password"]):
            user.password_hash = bcrypt.generate_password_hash(
                data["newPassword"]
            ).decode("utf-8")
            db.session.commit()
            return make_response({"message": "Password updated successfully"}, 200)
        else:
            return make_response({"error": "Invalid credentials"}, 401)


class UserLoginResource(Resource):
    """
    Handles user login requests by validating provided credentials.
    Successful login creates a user session.
    """

    def post(self):
        """Authenticates user with provided username and password, creating a session on success."""

        data = request.get_json()
        if not data or "username" not in data or "password" not in data:
            return make_response(
                jsonify({"error": "Username and password are required"}), 400
            )

        user = UserAuth.query.filter_by(username=data["username"].lower()).first()
        if user and user.check_password(
            data["password"]
        ):  # Utilize the check_password method of the UserAuth model
            session["user_id"] = user.id
            session["username"] = user.username
            session["logged_in"] = True

            # Create a new UserSession instance
            new_user_session = UserSession(
                user_id=user.id, started_at=datetime.utcnow()
            )
            db.session.add(new_user_session)
            db.session.commit()

            session["session_id"] = new_user_session.id

            response_data = {
                "message": "Login successful",
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "session_id": new_user_session.id,
            }

            return make_response(jsonify(response_data), 200)
        else:
            return make_response(
                jsonify({"error": "Invalid username or password"}), 401
            )


class UserLogoutResource(Resource):
    """
    Manages user logout process, clearing the session.
    """

    def post(self):
        """
        Handles the logout process for users.
        Before clearing the Flask session, it marks the user's current session as ended.
        """
        user_id = session.get("user_id")

        if user_id:
            current_session = (
                UserSession.query.filter_by(user_id=user_id, ended_at=None)
                .order_by(UserSession.started_at.desc())
                .first()
            )
            if current_session:
                current_session.ended_at = datetime.utcnow()
                db.session.commit()

        session.clear()

        response = make_response(jsonify({"message": "Logout successful"}), 200)
        response.set_cookie("session", "", expires=0)
        return response


class SessionCheckResource(Resource):
    """
    Checks if there's an active session, indicating an authenticated user.
    """

    def get(self):
        """Returns user information if authenticated, otherwise indicates no active session."""

        try:
            user_id = session.get("user_id")
            if user_id:
                user = UserAuth.query.get(user_id)
                if user:
                    return (
                        jsonify(
                            {
                                "authenticated": True,
                                "id": user.id,
                                "username": user.username,
                                "email": user.email,
                            }
                        ),
                        200,
                    )
                else:
                    return (
                        jsonify({"authenticated": False, "message": "User not found"}),
                        404,
                    )
            else:
                return jsonify({"authenticated": False}), 200
        except Exception as e:
            logging.error(f"Error in SessionCheckResource: {str(e)}")
            return jsonify({"error": "Internal server error", "details": str(e)}), 500


# Shipping Information Resources
# -------------------------------
class ShippingInfoSchema(ma.SQLAlchemyAutoSchema):
    """
    Resource for managing shipping information associated with user accounts.
    Supports retrieving, creating, and updating shipping information.
    """

    class Meta:
        model = ShippingInfo
        sqla_session = db.session


class ShippingInfoResource(Resource):
    def get(self, user_id):
        """
        Retrieves shipping information for a given user ID, ensuring that the requestor has the right to access the information.
        """
        session_user_id = session.get("user_id")
        if not session_user_id or str(session_user_id) != str(user_id):
            return {"error": "Unauthorized access or user not found"}, 403

        shipping_info = ShippingInfo.query.filter_by(user_id=user_id).first()
        if not shipping_info:
            return {"error": "Shipping information not found"}, 404

        schema = ShippingInfoSchema()
        return schema.dump(shipping_info), 200

    def post(self):
        """
        Creates or updates shipping information for the current user session from provided JSON data.
        Validates required fields and data integrity before saving to the database.
        """
        shipping_data = request.get_json()
        if not shipping_data:
            return make_response(jsonify({"error": "No data provided"}), 400)

        required_fields = [
            "address_line1",
            "city",
            "state",
            "postal_code",
            "country",
            "phone_number",
        ]
        missing_fields = [
            field for field in required_fields if field not in shipping_data
        ]
        if missing_fields:
            return make_response(
                jsonify(
                    {"error": "Missing data for fields: " + ", ".join(missing_fields)}
                ),
                400,
            )

        try:
            shipping_info = ShippingInfo(
                address_line1=shipping_data["address_line1"],
                address_line2=shipping_data.get("address_line2", ""),
                city=shipping_data["city"],
                state=shipping_data["state"],
                postal_code=shipping_data["postal_code"],
                country=shipping_data["country"],
                phone_number=shipping_data["phone_number"],
            )
            db.session.add(shipping_info)
            db.session.commit()

            response_data = {
                "id": shipping_info.id,
                "address_line1": shipping_info.address_line1,
                "address_line2": shipping_info.address_line2,
                "city": shipping_info.city,
                "state": shipping_info.state,
                "postal_code": shipping_info.postal_code,
                "country": shipping_info.country,
                "phone_number": shipping_info.phone_number,
            }

            return make_response(
                jsonify(
                    {
                        "message": "Shipping info added successfully",
                        "shippingInfo": response_data,
                    }
                ),
                201,
            )

        except KeyError as e:
            return make_response(jsonify({"error": f"Missing field in data: {e}"}), 400)
        except Exception as e:
            db.session.rollback()
            return make_response(
                jsonify({"error": "Failed to add shipping info", "details": str(e)}),
                500,
            )

    def patch(self):
        """
        Updates an existing shipping information record for the current user session.
        Allows partial updates to shipping information fields.
        """
        user_id = session.get("user_id")
        if not user_id:
            return {"error": "Authentication required"}, 401

        user = UserAuth.query.get(user_id)
        if not user or not user.shipping_info:
            return {"error": "Shipping info not found or unauthorized"}, 404

        shipping_data = request.get_json()
        shipping_info = user.shipping_info
        for field in [
            "address_line1",
            "address_line2",
            "city",
            "state",
            "postal_code",
            "country",
            "phone_number",
        ]:
            if field in shipping_data:
                setattr(shipping_info, field, shipping_data[field])

        db.session.commit()
        return {"message": "Shipping info updated successfully"}, 200


# Product Management Resources
# -----------------------------
class ProductSchema(ma.SQLAlchemyAutoSchema):
    """
    Marshmallow schema for Product model.
    Facilitates serialization of Product instances for API responses and deserialization of request data to Product model instances.
    Includes custom methods for price conversion between dollars and cents to handle financial data accurately.
    """

    class Meta:
        model = Product
        sqla_session = db.session

    price_in_dollars = fields.Method(
        deserialize="price_to_cents", serialize="cents_to_dollars"
    )

    def price_to_cents(self, value):
        """
        Deserialization method to convert price from dollars to cents.
        Ensures the price is stored in the smallest currency unit for precision.
        """
        try:
            return int(float(value) * 100)
        except ValueError:
            raise ValidationError("Price must be a valid number.")

    def cents_to_dollars(self, obj):
        """
        Serialization method to convert price from cents to dollars.
        Provides a user-friendly price format in API responses.
        """
        return f"${obj.price / 100:.2f}"

    quantity = fields.Integer(
        validate=validate.Range(min=1),
        required=True,
        error_messages={
            "required": "Quantity is required.",
            "invalid": "Quantity must be a positive integer.",
        },
    )


class ProductResource(Resource):
    """
    Resource for managing Product entities, supporting CRUD operations.
    """

    def get(self, product_id=None):
        """
        Retrieves a single product by ID or all products if no ID is provided.
        Includes product colors in the response for comprehensive product details.
        """
        if product_id:
            product = Product.query.get_or_404(product_id)
            return jsonify(product.to_dict(include_colors=True))
        else:
            products = Product.query.all()
            return jsonify([product.to_dict() for product in products])

    def post(self):
        """
        Creates a new product from JSON request data, validating against ProductSchema.
        """
        schema = ProductSchema()
        try:
            product_data = schema.load(request.get_json())
            product = Product(**product_data)
            db.session.add(product)
            db.session.commit()
            return {
                "message": "Product created successfully",
                "product": schema.dump(product),
            }, 201
        except ValidationError as err:
            return {"errors": err.messages}, 400
        except IntegrityError:
            db.session.rollback()
            return {"error": "Could not create the product due to internal error."}, 500

    def patch(self, product_id):
        """
        Updates an existing product identified by product_id with provided JSON data.
        """
        product_data = request.get_json()
        product = Product.query.get(product_id)
        if not product:
            return make_response({"error": "Product not found"}, 404)

        product.name = product_data.get("name", product.name)
        product.description = product_data.get("description", product.description)
        product.price = product_data.get("price", product.price)
        product.image_path = product_data.get("image_path", product.image_path)
        product.imageAlt = product_data.get("imageAlt", product.imageAlt)

        db.session.commit()
        return make_response({"message": "Product updated successfully"}, 200)

    def delete(self, product_id):
        """
        Deletes an existing product identified by product_id.
        """
        product = Product.query.get(product_id)
        if not product:
            return make_response({"error": "Product not found"}, 404)

        db.session.delete(product)
        db.session.commit()
        return make_response({"message": "Product deleted successfully"}, 200)


# Color Resource
class ColorResource(Resource):
    """
    Resource for managing Color entities in the database, supporting operations such as retrieval, creation, and deletion of color options.
    """

    def get(self, color_id):
        """
        Retrieves a specific color by its ID and returns its details.
        """
        color = Color.query.get_or_404(color_id)
        return make_response(color.to_dict(), 200)

    def post(self):
        """
        Creates a new color entry from JSON request data.
        Validates the presence of 'name' field in the data.
        """
        data = request.get_json()
        new_color = Color(name=data["name"])
        db.session.add(new_color)
        db.session.commit()
        return make_response(new_color.to_dict(), 201)

    def delete(self, color_id):
        """
        Deletes an existing color by its ID.
        """
        color = Color.query.get_or_404(color_id)
        db.session.delete(color)
        db.session.commit()
        return make_response({"message": "Color deleted successfully"}, 200)


# Order Resource
class OrderResource(Resource):
    """
    Resource for managing Order entities, facilitating operations like retrieval, creation, and deletion of orders.
    """

    def get(self, order_id):
        """
        Retrieves and returns details of a specific order by its ID.
        """
        order = Order.query.get_or_404(order_id)
        return jsonify(order.serialize())

    def post(self):
        """
        Creates a new order based on JSON request data. Associates the order with the user's session ID and specified shipping information.
        Validates the presence of 'order_details' in the request data.
        """
        try:
            data = request.get_json()

            new_order = Order(
                user_id=session.get("user_id"),
                shipping_info_id=data.get("shipping_info_id"),
            )
            db.session.add(new_order)
            db.session.flush()

            for detail in data["order_details"]:
                order_detail = OrderDetail(
                    order_id=new_order.id,
                    product_id=detail["product_id"],
                    quantity=detail["quantity"],
                    color_id=detail.get("color_id"),
                )
                db.session.add(order_detail)

            db.session.commit()
            return make_response(
                {
                    "message": "Order created successfully",
                    "order": new_order.serialize(),
                },
                201,
            )

        except Exception as e:
            db.session.rollback()
            print("Error:", str(e))
            return make_response({"error": "An unexpected error occurred"}, 500)

    def delete(self, order_id):
        """
        Deletes an order by its ID, ensuring the associated order details are also removed.
        """
        order = Order.query.get_or_404(order_id)
        db.session.delete(order)
        db.session.commit()
        return make_response({"message": "Order deleted successfully"}, 200)


# Chat Functionality Resources
# -----------------------------


class ChatMessageSchema(ma.SQLAlchemyAutoSchema):
    """
    Marshmallow schema for serializing and deserializing ChatMessage entities.
    This schema facilitates the conversion of chat messages to and from JSON format,
    ensuring the data integrity of chat functionalities.
    """

    class Meta:
        model = ChatMessage
        load_instance = True
        fields = (
            "id",
            "user_id",
            "message",
            "response",
            "request_data",
            "response_data",
            "timestamp",
        )


chat_message_schema = ChatMessageSchema()


def read_support_guide(file_path=file_path):
    """
    Reads the support guide from a specified file path, providing a system message
    to be included in chat sessions for guidance.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            support_guide = file.read()
        return support_guide
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
    return ""


def get_completion(
    user_id, user_message, model="gpt-3.5-turbo", temperature=0.7, max_tokens=150
):
    """
    Fetches AI-generated responses based on the user's message and preceding chat context.
    Utilizes OpenAI's API to generate responses tailored to the conversation flow.
    """
    # Retrieve the last three messages for context
    last_messages = (
        ChatMessage.query.filter_by(user_id=user_id)
        .order_by(ChatMessage.timestamp.desc())
        .limit(3)
        .all()
    )
    support_guide = read_support_guide()

    # Construct the message payload including the system message, previous messages, and the current user message
    messages = (
        [
            {"role": "system", "content": support_guide},
        ]
        + [
            {
                "role": "user" if msg.user_id == user_id else "assistant",
                "content": msg.message or msg.response,
            }
            for msg in reversed(last_messages)
        ]
        + [
            {"role": "user", "content": user_message},
        ]
    )

    try:
        # Generate the completion using the OpenAI API
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        if response.choices and response.choices[0].message:
            return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error: {e}")
    return None


@app.route("/api/chat_messages", methods=["POST"])
def chat():
    """
    Endpoint to handle the posting of new chat messages. Processes the user's message,
    generates an AI response, and stores the conversation in the database.
    """
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "You must be signed in to send messages."}), 403

    current_session = (
        UserSession.query.filter_by(user_id=user_id, ended_at=None)
        .order_by(UserSession.started_at.desc())
        .first()
    )
    session_id = current_session.id if current_session else None

    data = request.json
    user_message = data.get("message")
    if not user_message:
        return jsonify({"error": "No message provided."}), 400

    ai_response = get_completion(user_id, user_message)

    if ai_response:
        new_chat_message = ChatMessage(
            user_id=user_id,
            session_id=session_id,
            message=user_message,
            response=ai_response,
        )

        db.session.add(new_chat_message)
        db.session.commit()

        result = chat_message_schema.dump(new_chat_message)
        return jsonify(result), 200
    else:
        return jsonify({"error": "Failed to get response from AI"}), 500


@app.route("/api/continue_last_conversation", methods=["GET"])
def continue_last_conversation():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "User not logged in."}), 401
    print("user_id", user_id)

    last_session_id = (
        db.session.query(ChatMessage.session_id)
        .filter(ChatMessage.user_id == user_id)
        .order_by(ChatMessage.timestamp.desc())
        .first()
    )

    if not last_session_id:
        return jsonify({"error": "No previous session found."}), 404

    last_session_id = last_session_id[0]
    last_session = UserSession.query.get(last_session_id)

    if not last_session:
        return jsonify({"error": "No previous session found."}), 404

    print("last_session", last_session)
    print("last_session.id", last_session.id)

    chat_messages = (
        ChatMessage.query.filter_by(session_id=last_session_id)
        .order_by(ChatMessage.timestamp.asc())
        .all()
    )
    print("chat_messages", chat_messages)

    if not chat_messages:
        return jsonify({"message": "No messages found in the last session."}), 200

    messages = []
    for chat_message in chat_messages:
        user_message = {"sender": "user", "text": chat_message.message}
        ai_response = {"sender": "bot", "text": chat_message.response}
        messages.extend([user_message, ai_response])

    return jsonify({"session_id": last_session.id, "messages": messages}), 200


# API Resource Routing
# --------------------
# supporting functionalities like user authentication, product management, and order processing.

# User Authentication Endpoints
api.add_resource(UserLoginResource, "/api/login")
api.add_resource(UserLogoutResource, "/api/logout")
api.add_resource(UserAuthResource, "/api/user_auth")
# Shipping Information Endpoints
api.add_resource(ShippingInfoResource, "/api/shipping_info")
# Product Management Endpoints
api.add_resource(ProductResource, "/api/product", "/api/product/<int:product_id>")
# Color Management Endpoints
api.add_resource(ColorResource, "/api/colors", "/api/colors/<int:color_id>")
# Order Management Endpoints
api.add_resource(OrderResource, "/api/orders", "/api/orders/<int:order_id>")
# Session Management Endpoint
api.add_resource(SessionCheckResource, "/api/check_session")


if __name__ == "__main__":
    app.run(port=5555, debug=True)
