#!/usr/bin/env python3

# Standard library imports
import logging
import os
import traceback
from calendar import c
from time import sleep

import bcrypt

# from app_utils import create_assistant
from config import api, app, db, ma
from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, request, session
from flask_bcrypt import Bcrypt, check_password_hash, generate_password_hash
from flask_marshmallow import fields
from flask_restful import Resource, reqparse
from marshmallow import Schema, ValidationError, fields, post_dump, validate
from models import (
    ChatMessage,
    Color,
    Order,
    OrderDetail,
    Product,
    ShippingInfo,
    UserAuth,
)

# from openai import OpenAI
# from packaging import version
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

# Local imports


# Builds app, set attributes
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'app.db')}"
)
load_dotenv()
app.secret_key = os.environ.get("SECRET_KEY")

bcrypt = Bcrypt(app)


@app.route("/")
def index():
    return "<h1>ChatPoweredEcommerce</h1>"


class UserAuthSchema(ma.SQLAlchemyAutoSchema):
    """
    A Marshmallow schema for serializing and deserializing UserAuth instances.
    This schema is used for validating user input upon registration and for output formatting.
    Excludes the password_hash field from the serialized output for security reasons.
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
    Resource for managing UserAuth entities including retrieval, creation, deletion,
    """

    def get(self):
        """
        Retrieves and returns all user records, excluding their password hashes.
        """
        users = UserAuth.query.all()
        user_schema = UserAuthSchema(many=True, only=["id", "username", "email"])
        return make_response(jsonify(user_schema.dump(users)), 200)

    def post(self):
        user_data = request.get_json()

        if not user_data:
            return make_response(jsonify({"error": "No input data provided"}), 400)

        username = user_data.get("username")
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

        session["user_id"] = new_user.id
        session["username"] = new_user.username
        session["logged_in"] = True

        return make_response(
            jsonify(
                {
                    "message": "User created successfully and logged in",
                    "id": new_user.id,
                    "username": new_user.username,
                    "email": new_user.email,
                }
            ),
            201,
        )

    def delete(self):
        """
        Deletes a user after validating their credentials.
        """
        try:
            data = request.get_json()
            if not all(key in data for key in ("username", "password")):
                return make_response(
                    {"error": "Username and password are required"}, 400
                )

            username = data["username"]
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
        """
        Updates a user's password after validating the current password.
        """
        data = request.get_json()
        user = UserAuth.query.filter_by(username=data["username"]).first()
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
    Handles user login requests. Validates provided credentials
    """

    def post(self):
        data = request.get_json()
        # Check if both username and password are provided
        if not data or "username" not in data or "password" not in data:
            return make_response(
                jsonify({"error": "Username and password are required"}), 400
            )

        user = UserAuth.query.filter_by(username=data["username"]).first()

        # Initialize bcrypt
        bcrypt = Bcrypt()

        if user and bcrypt.check_password_hash(user.password_hash, data["password"]):
            session["user_id"] = user.id
            session["username"] = user.username
            session["logged_in"] = True

            response_data = {
                "message": "Login successful",
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
            }

            return make_response(jsonify(response_data), 200)
        else:
            return make_response(
                jsonify({"error": "Invalid username or password"}), 401
            )


class UserLogoutResource(Resource):
    def post(self):
        """
        Handles the logout process for users.

        Upon logout:
        - Clears the Flask session to remove any stored user information.
        """
        session.clear()
        return jsonify(message="Logout successful"), 200


# @app.errorhandler(Exception)
# def handle_unexpected_error(error):
#     return (
#         jsonify({"error": "An unexpected error occurred", "details": str(error)}),
#         500,
#     )


class SessionCheckResource(Resource):
    def get(self):
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


# User Tested Methods with Insomnia/Postman


class ShippingInfoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ShippingInfo
        sqla_session = db.session


class ShippingInfoResource(Resource):
    def get(self, user_id):
        session_user_id = session.get("user_id")
        if not session_user_id or str(session_user_id) != str(user_id):
            return {"error": "Unauthorized access or user not found"}, 403

        shipping_info = ShippingInfo.query.filter_by(user_id=user_id).first()
        if not shipping_info:
            return {"error": "Shipping information not found"}, 404

        schema = ShippingInfoSchema()
        return schema.dump(shipping_info), 200

    def post(self):
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


class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        sqla_session = db.session

    price_in_dollars = fields.Method(
        deserialize="price_to_cents", serialize="cents_to_dollars"
    )

    def price_to_cents(self, value):
        try:
            # Assume value is a string in dollar format, e.g., "12.99"
            return int(float(value) * 100)
        except ValueError:
            raise ValidationError("Price must be a valid number.")

    def cents_to_dollars(self, obj):
        return f"${obj.price / 100:.2f}"

    quantity = fields.Integer(
        validate=validate.Range(min=1),
        required=True,
        error_messages={
            "required": "Quantity is required.",
            "invalid": "Quantity must be a positive integer.",
        },
    )


# Product Resource handling with JWT for certain operations
class ProductResource(Resource):
    def get(self, product_id=None):
        if product_id:
            product = Product.query.get_or_404(product_id)
            return jsonify(product.to_dict(include_colors=True))
        else:
            products = Product.query.all()
            return jsonify([product.to_dict() for product in products])

    def post(self):
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
        product = Product.query.get(product_id)
        if not product:
            return make_response({"error": "Product not found"}, 404)

        db.session.delete(product)
        db.session.commit()
        return make_response({"message": "Product deleted successfully"}, 200)


# Color Resource
class ColorResource(Resource):
    def get(self, color_id):
        color = Color.query.get_or_404(color_id)
        return make_response(color.to_dict(), 200)

    def post(self):
        data = request.get_json()
        new_color = Color(name=data["name"])
        db.session.add(new_color)
        db.session.commit()
        return make_response(new_color.to_dict(), 201)

    def delete(self, color_id):
        color = Color.query.get_or_404(color_id)
        db.session.delete(color)
        db.session.commit()
        return make_response({"message": "Color deleted successfully"}, 200)


# Order Resource
class OrderResource(Resource):

    def get(self, order_id):
        order = Order.query.get_or_404(order_id)
        return jsonify(order.serialize())

    def post(self):
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
        order = Order.query.get_or_404(order_id)
        db.session.delete(order)
        db.session.commit()
        return make_response({"message": "Order deleted successfully"}, 200)


# --------------------------------- Chatbot Resource ---------------------------------#
# Check OpenAI version is correct
# required_version = version.parse("1.1.1")
# current_version = version.parse(openai.__version__)
# OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
# if current_version < required_version:
#     raise ValueError(
#         f"Error: OpenAI version {openai.__version__}"
#         " is less than the required version 1.1.1"
#     )
# else:
#     print("OpenAI version is compatible.")

# # Init client
# client = OpenAI(api_key=OPENAI_API_KEY)

# # Create new assistant or load existing
# assistant_id = create_assistant(client)


# # Start conversation thread
# class OpenAIStartConversation(Resource):
#     def start_conversation():
#         print("Starting a new conversation...")  # Debugging line
#         thread = client.beta.threads.create()
#         print(f"New thread created with ID: {thread.id}")  # Debugging line
#         return jsonify({"thread_id": thread.id})


# # Generate response
# class OpenAIChat(Resource):
#     def chat():
#         data = request.json
#         thread_id = data.get("thread_id")
#         user_input = data.get("message", "")

#         if not thread_id:
#             print("Error: Missing thread_id")  # Debugging line
#             return jsonify({"error": "Missing thread_id"}), 400

#         print(
#             f"Received message: {user_input} for thread ID: {thread_id}"
#         )  # Debugging line

#         # Add the user's message to the thread
#         client.beta.threads.messages.create(
#             thread_id=thread_id, role="user", content=user_input
#         )

#         # Run the Assistant
#         run = client.beta.threads.runs.create(
#             thread_id=thread_id, assistant_id=assistant_id
#         )

#         # Check if the Run requires action (function call)
#         while True:
#             run_status = client.beta.threads.runs.retrieve(
#                 thread_id=thread_id, run_id=run.id
#             )
#             print(f"Run status: {run_status.status}")
#             if run_status.status == "completed":
#                 break
#             sleep(1)  # Wait for a second before checking again

#         # Retrieve and return the latest message from the assistant
#         messages = client.beta.threads.messages.list(thread_id=thread_id)
#         response = messages.data[0].content[0].text.value

#         print(f"Assistant response: {response}")  # Debugging line
#         return jsonify({"response": response})


# ChatMessage Resource
class ChatMessageResource(Resource):
    def get(self, message_id):
        message = ChatMessage.query.get_or_404(message_id)
        return make_response(message.to_dict(), 200)

    def post(self):
        data = request.get_json()
        new_message = ChatMessage(
            user_id=data["user_id"],
            message=data["message"],
            response=data.get("response", ""),
        )
        db.session.add(new_message)
        db.session.commit()
        return make_response(new_message.to_dict(), 201)


# Routing
# api.add_resource(OpenAIStartConversation, "/start")
# api.add_resource(OpenAIChat, "/chat")
api.add_resource(UserLoginResource, "/login")
api.add_resource(UserLogoutResource, "/logout")
api.add_resource(UserAuthResource, "/user_auth")
api.add_resource(ShippingInfoResource, "/shipping_info")
api.add_resource(ProductResource, "/product", "/product/<int:product_id>")
api.add_resource(ColorResource, "/colors", "/colors/<int:color_id>")
api.add_resource(
    ChatMessageResource, "/chat_messages", "/chat_messages/<int:message_id>"
)
api.add_resource(OrderResource, "/orders", "/orders/<int:order_id>")
api.add_resource(SessionCheckResource, "/check_session")


if __name__ == "__main__":
    app.run(port=5555, debug=True)
