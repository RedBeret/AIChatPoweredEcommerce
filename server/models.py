import re  # Regular expression library for email validation
import uuid
from datetime import datetime

# Import utility functions for validation and currency conversion
from app_utils import (
    cents_to_dollar,
    dollar_to_cents,
    validate_not_blank,
    validate_positive_number,
)
from config import bcrypt, db  # Configuration for database and bcrypt for hashing
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin


# UserAuth model to store user authentication details like username, email, and password hash.
# Includes relationships for related data such as chat messages, shipping information, and orders.
class UserAuth(db.Model, SerializerMixin):
    __tablename__ = "user_auth"  # Specifies the table name in the database

    # Primary Key and fields with uniqueness constraints to avoid duplicate entries
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    # Defining relationships with other models to enable easy data retrieval
    chat_messages = db.relationship(
        "ChatMessage", back_populates="user", cascade="all, delete-orphan"
    )

    openai_interactions = db.relationship("OpenAIInteraction", back_populates="user")
    orders = db.relationship("Order", back_populates="user")

    @validates("email")
    def validate_email(self, key, address):
        # Validate email format
        assert re.match("[^@]+@[^@]+\.[^@]+", address), "Invalid email address"
        # Validate email length
        assert len(address) >= 3, f"{key} must be at least 3 characters long"
        return address

    @validates("username")
    def validate_username(self, key, value):
        # Validate username length
        assert len(value) >= 3, f"{key} must be at least 3 characters long"
        return value

    # Ensures password field is write-only for security reasons
    @hybrid_property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    # Hashes password before storing in the database
    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    # Verifies password against the hash stored in the database
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    serialize_rules = (
        "-password_hash",
        "-chat_messages.user",
    )  # Excludes password_hash from serialization to enhance security


# ShippingInfo model to store user shipping details.
# Linked to UserAuth model to establish a one-to-one relationship.
class ShippingInfo(db.Model, SerializerMixin):
    __tablename__ = "shipping_info"

    # Standard fields for storing address information
    id = db.Column(db.Integer, primary_key=True)
    address_line1 = db.Column(db.String(255), nullable=False)
    address_line2 = db.Column(db.String(255))
    city = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(255), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)

    @validates("postal_code")
    def validate_postal_code(self, key, code):
        assert re.match("^\d{5}(-\d{4})?$", code), "Invalid postal code format"
        return code

    @validates("phone_number")
    def validate_phone_number(self, key, number):
        assert re.match("^\+?1?\d{9,15}$", number), "Invalid phone number format"
        return number

    def __repr__(self):
        return f"<ShippingInfo {self.id} for User {self.user_id}>"


# Product model to represent individual products.
# Includes fields for product details and relationships for colors and product colors.
class Product(db.Model, SerializerMixin):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    item_quantity = db.Column(db.Integer, nullable=False, default=0)
    price = db.Column(db.Integer, nullable=False)  # Stored in cents for precision
    image_path = db.Column(db.String(255), nullable=True)
    imageAlt = db.Column(db.String(255), nullable=True)
    colors = db.relationship(
        "Color", secondary="product_colors", back_populates="products"
    )

    @hybrid_property
    def price_in_dollars(self):
        return self.price / 100

    # Validation methods ensure data integrity before saving to database
    @validates("name", "description", "image_path", "imageAlt", "item_quantity")
    def validate_field(self, key, value):
        # Specific logic for validating item quantity, ensuring it's a positive integer
        if key == "item_quantity":
            value = validate_positive_number(value, key)
        else:  # For other fields, ensures they are not blank
            validate_not_blank(value, key)
        return value

    @validates("price")
    def validate_price(self, key, price):
        # Ensures price is a positive number before converting and storing in cents
        price_in_cents = validate_positive_number(price, key)
        return price_in_cents

    def to_dict(self, include_colors=False):
        data = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "item_quantity": self.item_quantity,
            "image_path": self.image_path,
            "imageAlt": self.imageAlt,
        }

        if include_colors:
            data["colors"] = [
                {"id": color.id, "name": color.name} for color in self.colors
            ]

        return data

    serialize_rules = (
        "-price",
        "price_in_dollars",
    )

    def __repr__(self):
        return f"<Product {self.name}>"


# Represents a color option for products. Each color has a unique name and can be associated with multiple products.
class Color(db.Model, SerializerMixin):
    __tablename__ = "colors"

    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each color
    name = db.Column(
        db.String(255), unique=True, nullable=False
    )  # Color name must be unique

    # Many-to-many relationship with Product model. A color can belong to many products and vice versa.
    products = db.relationship(
        "Product", secondary="product_colors", back_populates="colors"
    )

    def __repr__(self):
        # Representation method for easier identification of color objects in logs and debugging sessions.
        return f"<Color {self.name}>"


# Association table to represent the many-to-many relationship between products and colors.
class ProductColor(db.Model):
    __tablename__ = "product_colors"

    product_id = db.Column(
        db.Integer, db.ForeignKey("products.id"), primary_key=True
    )  # FK to Product
    color_id = db.Column(
        db.Integer, db.ForeignKey("colors.id"), primary_key=True
    )  # FK to Color

    def __repr__(self):
        # Provides a clear text representation of the relationship for logging and debugging.
        return (
            f"<ProductColor Product ID: {self.product_id}, Color ID: {self.color_id}>"
        )


# Represents an order placed by a user, containing details like creation time and confirmation number.
class Order(db.Model, SerializerMixin):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each order
    user_id = db.Column(
        db.Integer, db.ForeignKey("user_auth.id"), nullable=False
    )  # Link to the user who placed the order
    created_at = db.Column(
        db.DateTime, default=db.func.current_timestamp()
    )  # Timestamp of order creation
    confirmation_num = db.Column(db.String(36), unique=True, nullable=False)
    # Unique confirmation number

    # ForeignKey relationship to ShippingInfo for delivery details
    shipping_info_id = db.Column(
        db.Integer, db.ForeignKey("shipping_info.id"), nullable=True
    )
    shipping_info = db.relationship("ShippingInfo")
    # Relationship to OrderDetail for storing individual items within the order
    order_details = db.relationship(
        "OrderDetail", back_populates="order", cascade="all, delete-orphan"
    )
    user = db.relationship(
        "UserAuth", back_populates="orders"
    )  # Links back to the user for easy access to their orders

    products = association_proxy("order_details", "product")

    serialize_rules = (
        "-user",
        "-order_details.product.order_details",
        "-order_details.order",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.confirmation_num = str(uuid.uuid4())

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "shipping_info_id": self.shipping_info_id,
            "confirmation_num": self.confirmation_num,
            "order_details": [detail.serialize() for detail in self.order_details],
        }

    def __repr__(self):
        # Representation includes the order ID and the user ID for clarity.
        return f"<Order {self.id} User ID: {self.user_id}>"


# Stores individual items within an order, including product ID and quantity.
class OrderDetail(db.Model, SerializerMixin):
    __tablename__ = "order_details"

    id = db.Column(
        db.Integer, primary_key=True
    )  # Unique identifier for each order detail
    order_id = db.Column(
        db.Integer, db.ForeignKey("orders.id"), nullable=False
    )  # Link to the parent order
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.id"), nullable=False
    )  # Product being ordered
    quantity = db.Column(db.Integer, nullable=False)
    color_id = db.Column(db.Integer, db.ForeignKey("colors.id"))
    color = db.relationship("Color")
    order = db.relationship(
        "Order", back_populates="order_details"
    )  # Relationship back to the order
    product = db.relationship(
        "Product"
    )  # Links to the product for easy access to product details
    serialize_rules = ("-order", "-product.order_details")

    def serialize(self):
        serialized_data = {
            "id": self.id,
            "order_id": self.order_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "color_id": self.color_id,
        }

        # Check if product is not None before accessing its attributes
        if self.product is not None:
            serialized_data["product"] = {
                "id": self.product.id,
                "name": self.product.name,
            }
        else:
            serialized_data["product"] = {"id": None, "name": "Unknown"}

        # Check if color is not None before accessing its attributes
        if self.color is not None:
            serialized_data["color"] = {"id": self.color.id, "name": self.color.name}
        else:
            serialized_data["color"] = {"id": None, "name": "Unknown"}

        return serialized_data

    def __repr__(self):
        # Provides clarity on the order detail's composition for debugging and logging.
        return f"<OrderDetail Order ID: {self.order_id}, Product ID: {self.product_id}, Quantity: {self.quantity}>"


# ChatMessage model captures messages between users and the system, storing content and timestamps.
class ChatMessage(db.Model, SerializerMixin):
    __tablename__ = "chat_messages"

    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each message
    user_id = db.Column(
        db.Integer, db.ForeignKey("user_auth.id"), nullable=False
    )  # Link to the user who sent/received the message
    message = db.Column(db.Text, nullable=False)  # Content of the message
    response = db.Column(db.Text, nullable=False)  # System response to the message
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False
    )  # Timestamp of the message exchange

    user = db.relationship(
        "UserAuth", back_populates="chat_messages"
    )  # Links back to the user involved in the chat

    def __repr__(self):
        # Representation to easily identify message exchanges in logs.
        return f"<ChatMessage {self.id} User ID: {self.user_id}>"


# AITrainingData model stores data points collected for AI training purposes, including creation timestamps.
class AITrainingData(db.Model, SerializerMixin):
    __tablename__ = "ai_training_data"

    id = db.Column(
        db.Integer, primary_key=True
    )  # Unique identifier for each data point
    data = db.Column(
        db.Text, nullable=False
    )  # The actual data being stored for AI training
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False
    )  # Timestamp of data creation

    def __repr__(self):
        # Representation to easily identify AI training data entries.
        return f"<AITrainingData {self.id}>"


# OpenAIInteraction model captures interactions with OpenAI's API, including request and response data.
class OpenAIInteraction(db.Model, SerializerMixin):
    __tablename__ = "openai_interactions"

    id = db.Column(
        db.Integer, primary_key=True
    )  # Unique identifier for each interaction
    user_id = db.Column(
        db.Integer, db.ForeignKey("user_auth.id"), nullable=True
    )  # Optional link to the user initiating the interaction
    request_data = db.Column(db.Text, nullable=False)  # Data sent to OpenAI API
    response_data = db.Column(db.Text, nullable=False)  # Data received from OpenAI API
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False
    )  # Timestamp of the interaction

    user = db.relationship(
        "UserAuth", back_populates="openai_interactions"
    )  # Links back to the user, if applicable

    def __repr__(self):
        # Provides a concise summary of the interaction for logging and debugging purposes.
        return f"<OpenAIInteraction {self.id} User ID: {self.user_id}>"
