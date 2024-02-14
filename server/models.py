# models.py: Defines the database models for the AiChatPoweredEcommerce platform, including user authentication,
# shipping information, products, colors, orders, order details, ai chat messages, and AI training data.
# Utilizes Flask-SQLAlchemy for ORM, Bcrypt for password hashing, and custom validation methods to ensure data integrity.

import re
import uuid
from datetime import datetime

from app_utils import (
    cents_to_dollar,
    dollar_to_cents,
    validate_not_blank,
    validate_positive_number,
)
from config import bcrypt, db
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin


class UserAuth(db.Model, SerializerMixin):
    """
    UserAuth Model: Manages user authentication data and relations.

    Fields:
    - id: Primary key.
    - username: Unique username for user identification.
    - email: User's email address.
    - password_hash: Hashed password for secure storage.

    Relations:
    - chat_messages: User's chat history.
    - orders: Orders placed by the user.

    Validations:
    - email and username are validated for length and format.

    Security:
    - Passwords are hashed using bcrypt upon setting to ensure secure storage.
    - Password field is write-only to prevent unauthorized access.
    """

    __tablename__ = "user_auth"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    chat_messages = db.relationship(
        "ChatMessage", back_populates="user", cascade="all, delete-orphan"
    )
    sessions = db.relationship(
        "UserSession", back_populates="user", cascade="all, delete-orphan"
    )
    orders = db.relationship("Order", back_populates="user")

    @validates("email")
    def validate_email(self, key, address):
        """
        Validates the email address to ensure it follows a general email format and length.

        This validation is crucial for maintaining data integrity and ensuring that user notifications,
        password resets, and other communications are sent to a valid email address. The validation
        checks include ensuring the email address is at least 3 characters long and matches a basic
        pattern for email addresses. This is a simplistic check aimed at catching obvious errors, and
        it may be adjusted to use more sophisticated regex patterns or external validation libraries
        for comprehensive email validation in a production environment.
        """
        assert len(address) >= 3, f"{key} must be at least 3 characters long"
        assert re.match(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", address
        ), "Invalid email format"
        return address

    @validates("username")
    def validate_username(self, key, value):
        """
        Validates the username format and length.
        """
        assert len(value) >= 3, f"{key} must be at least 3 characters long"
        return value

    @hybrid_property
    def password(self):
        """
        Ensures password field is write-only for security reasons
        """
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        """
        Hashes the password before storing it in the database.
        """
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        """
        Verifies password against the hash stored in the database
        """
        return bcrypt.check_password_hash(self.password_hash, password)

    serialize_rules = (
        "-password_hash",
        "-chat_messages.user",
    )


class ShippingInfo(db.Model, SerializerMixin):
    """
    ShippingInfo Model: Stores shipping information for users.

    Fields:
    - id: Primary key.
    - address_line1/2: Address details.
    - city, state, postal_code, country: Location details.
    - phone_number: Contact information.

    Validation:
    - postal_code is validated against a standard format to ensure data integrity.

    Representation:
    - Provides clear identification for logging and debugging purposes.
    """

    __tablename__ = "shipping_info"

    id = db.Column(db.Integer, primary_key=True)
    address_line1 = db.Column(db.String(255), nullable=False)
    address_line2 = db.Column(db.String(255))
    city = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(255), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(50), nullable=False)

    @validates("postal_code")
    def validate_postal_code(self, key, code):
        """
        Validates the postal code format to adhere to standard postal code formats.

        This validation ensures the postal code matches expected patterns for postal codes,
        specifically looking for formats like '12345' or '12345-6789'. This is critical for
        ensuring accurate delivery information is captured and used for shipping purposes.
        The regex used here is designed to cover U.S. postal code formats, but it may need
        to be adapted for applications supporting international shipping to accommodate different
        postal code systems.
        """
        assert re.match(r"^\d{5}(-\d{4})?$", code), "Invalid postal code format"
        return code

    def __repr__(self):
        return f"<ShippingInfo {self.id} for User {self.user_id}>"


class Product(db.Model, SerializerMixin):
    """
    Represents a product in the e-commerce platform.

    Attributes:
    - id: Unique identifier.
    - name: Product name.
    - description: Detailed description.
    - item_quantity: Available stock.
    - price: Price in cents to maintain precision.
    - image_path: Path to the product image.
    - imageAlt: Alternative text for the product image.
    - colors: Relationship to Color model for available colors.

    Methods:
    - price_in_dollars: Converts price to dollars for display.
    - validate_field: Validates various fields for correctness.
    - to_dict: Serializes product data, optionally including colors.
    """

    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    item_quantity = db.Column(db.Integer, nullable=False, default=0)
    price = db.Column(db.Integer, nullable=False)
    image_path = db.Column(db.String(255), nullable=True)
    imageAlt = db.Column(db.String(255), nullable=True)
    colors = db.relationship(
        "Color", secondary="product_colors", back_populates="products"
    )

    @hybrid_property
    def price_in_dollars(self):
        return self.price / 100

    @validates("name", "description", "image_path", "imageAlt", "item_quantity")
    def validate_field(self, key, value):
        """
        Validates fields for non-blank values and positive numbers for 'item_quantity'.
        """
        if key == "item_quantity":
            value = validate_positive_number(value, key)
        else:  # For other fields, ensures they are not blank
            validate_not_blank(value, key)
        return value

    @validates("price")
    def validate_price(self, key, price):
        """
        Ensures price is a positive number before converting and storing in cents
        """

        price_in_cents = validate_positive_number(price, key)
        return price_in_cents

    def to_dict(self, include_colors=False):
        """
        Converts product details into a dictionary format, optionally including color information.
        Designed for flexible data representation in API responses.
        """
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


class Color(db.Model, SerializerMixin):
    """
    Represents a color option for products.

    Attributes:
    - id: Unique identifier for the color.
    - name: Color name, ensured unique across the platform.
    - products: Establishes a many-to-many relationship with the Product model, allowing products to have multiple color options and vice versa.

    Usage:
    - This model facilitates the categorization of products by color, enhancing the product discovery experience for users.
    """

    __tablename__ = "colors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

    products = db.relationship(
        "Product", secondary="product_colors", back_populates="colors"
    )

    def __repr__(self):
        return f"<Color {self.name}>"


class ProductColor(db.Model):
    """
    Association model linking products to colors in a many-to-many relationship.

    Attributes:
    - product_id: Foreign Key linking to the Product model.
    - color_id: Foreign Key linking to the Color model.

    This model enables products to have multiple color options and vice versa, enhancing product categorization and user experience.
    """

    __tablename__ = "product_colors"

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), primary_key=True)
    color_id = db.Column(db.Integer, db.ForeignKey("colors.id"), primary_key=True)

    def __repr__(self):
        return (
            f"<ProductColor Product ID: {self.product_id}, Color ID: {self.color_id}>"
        )


class Order(db.Model, SerializerMixin):
    """
    Represents an order made by a user, including details such as order creation time and a unique confirmation number.

    Attributes:
    - id: Unique identifier for the order.
    - user_id: Foreign Key to the UserAuth model, identifying the user who placed the order.
    - created_at: Timestamp when the order was created.
    - confirmation_num: A unique confirmation number generated for each order.
    - shipping_info_id: Foreign Key to the ShippingInfo model for delivery details.
    - order_details: Relationship to the OrderDetail model, detailing the items within the order.

    The model includes methods for serialization to facilitate data transfer and representation in API responses.
    """

    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_auth.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    confirmation_num = db.Column(db.String(36), unique=True, nullable=False)

    shipping_info_id = db.Column(
        db.Integer, db.ForeignKey("shipping_info.id"), nullable=True
    )
    shipping_info = db.relationship("ShippingInfo")
    order_details = db.relationship(
        "OrderDetail", back_populates="order", cascade="all, delete-orphan"
    )
    user = db.relationship("UserAuth", back_populates="orders")

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
        return f"<Order {self.id} User ID: {self.user_id}>"


class OrderDetail(db.Model, SerializerMixin):
    """
    Represents an item within an order, including references to the product, quantity, and selected color.

    Attributes:
    - id: Unique identifier for the order detail.
    - order_id: References the Order model, linking the detail to its parent order.
    - product_id: References the Product model, identifying the ordered product.
    - quantity: The quantity of the product ordered.
    - color_id: Optional reference to the Color model, specifying the selected color.
    """

    __tablename__ = "order_details"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    color_id = db.Column(db.Integer, db.ForeignKey("colors.id"))
    color = db.relationship("Color")
    order = db.relationship("Order", back_populates="order_details")
    product = db.relationship("Product")
    serialize_rules = ("-order", "-product.order_details")

    def serialize(self):
        """
        Serializes the order detail for API responses, including product and color information.
        """
        serialized_data = {
            "id": self.id,
            "order_id": self.order_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "color_id": self.color_id,
        }

        if self.product is not None:
            serialized_data["product"] = {
                "id": self.product.id,
                "name": self.product.name,
            }
        else:
            serialized_data["product"] = {"id": None, "name": "Unknown"}

        if self.color is not None:
            serialized_data["color"] = {"id": self.color.id, "name": self.color.name}
        else:
            serialized_data["color"] = {"id": None, "name": "Unknown"}

        return serialized_data

    def __repr__(self):
        return f"<OrderDetail Order ID: {self.order_id}, Product ID: {self.product_id}, Quantity: {self.quantity}>"


class UserSession(db.Model, SerializerMixin):
    """
    UserSession Model: Tracks user login sessions.

    Fields:
    - id: Primary key, auto-incremented. Used to identify the session uniquely.
    - user_id: Foreign key linking to the UserAuth model. Identifies the user owning the session.
    - started_at: Timestamp when the user logged in and the session was initiated.
    - ended_at: Timestamp when the user logged out, marking the session's end. Nullable, as sessions might be ongoing.

    Relations:
    - user: Defines the relationship back to the UserAuth model, allowing easy access to the user's data from a session.
    """

    __tablename__ = "user_sessions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_auth.id"), nullable=False)
    started_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    ended_at = db.Column(db.DateTime, nullable=True)

    user = db.relationship("UserAuth", back_populates="sessions")

    def __repr__(self):
        return f"<UserSession {self.id} User ID: {self.user_id}>"


class ChatMessage(db.Model, SerializerMixin):
    """
    Captures messages exchanged between the user and the system, including both user queries and system responses.

    Attributes:
    - id: Unique identifier for each chat message.
    - user_id: Links to the UserAuth model to identify the message's sender.
    - message: The content of the user's message.
    - response: The system's response to the user's message.
    - timestamp: The date and time when the message was exchanged.
    """

    __tablename__ = "chat_messages"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_auth.id"), nullable=False)
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey("user_sessions.id"), nullable=True)
    session = db.relationship("UserSession", backref="chat_messages")

    user = db.relationship("UserAuth", back_populates="chat_messages")

    def __repr__(self):
        return f"<ChatMessage {self.id} User ID: {self.user_id}>"


class AITrainingData(db.Model, SerializerMixin):
    """
    Represents AI training data points, storing the data used for AI model training along with timestamps.

    Attributes:
    - id: Primary key; unique identifier for each training data entry.
    - data: The training data content, stored as text.
    - created_at: Timestamp marking when the training data was created or recorded.
    """

    __tablename__ = "ai_training_data"

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<AITrainingData {self.id}>"
