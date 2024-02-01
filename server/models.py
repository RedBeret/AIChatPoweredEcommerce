from datetime import datetime

from config import bcrypt, db
from server.utilities import (
    normalize_price_input,
    validate_not_blank,
    validate_positive_number,
)
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin


# UserAuth model represents user authentication information.
class UserAuth(db.Model, SerializerMixin):
    __tablename__ = "user_auth"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    # Relationship to chat_messages
    chat_messages = db.relationship(
        "ChatMessage", back_populates="user", cascade="all, delete-orphan"
    )
    # Relationship to ShippingInfo
    shipping_info = db.relationship(
        "ShippingInfo", back_populates="user", uselist=False
    )

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    serialize_rules = ("-password_hash",)


# ShippingInfo model represents user shipping information.
class ShippingInfo(db.Model, SerializerMixin):
    __tablename__ = "shipping_info"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_auth.id"), nullable=False)
    address_line1 = db.Column(db.String(255), nullable=False)
    address_line2 = db.Column(db.String(255))
    city = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(255), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)

    user = db.relationship("UserAuth", back_populates="shipping_info")

    serialize_rules = ("-user",)


# Product model represents a product.
class Product(db.Model, SerializerMixin):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Integer, nullable=False)
    image_path = db.Column(db.String(255), nullable=True)
    imageAlt = db.Column(db.String(255), nullable=True)

    @validates("name")
    def validate_name(self, key, name):
        return validate_not_blank(name, key)

    @validates("price")
    def validate_price(self, key, price):
        price_in_cents = normalize_price_input(price)
        return validate_positive_number(price_in_cents, key)

    serialize_rules = ("-product_colors",)


# Color model represents a color.
class Color(db.Model, SerializerMixin):
    __tablename__ = "colors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    products = db.relationship(
        "Product", secondary="product_colors", back_populates="colors"
    )


# ProductColor model represents the relationship between products and colors.
class ProductColor(db.Model):
    __tablename__ = "product_colors"
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), primary_key=True)
    color_id = db.Column(db.Integer, db.ForeignKey("colors.id"), primary_key=True)


# Order model represents an order.
class Order(db.Model, SerializerMixin):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user_auth.id"), nullable=False
    )  # Make sure this matches your user table name
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    order_details = db.relationship(
        "OrderDetail", back_populates="order", cascade="all, delete-orphan"
    )
    user = db.relationship("UserAuth", back_populates="orders")


# OrderDetail model represents the details of an order.
class OrderDetail(db.Model, SerializerMixin):
    __tablename__ = "order_details"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    order = db.relationship("Order", back_populates="order_details")
    product = db.relationship("Product")

    serialize_rules = (
        "-order",
        "-product",
    )

    @validates("product_id")
    def validate_product_id(self, _, product_id):
        if not Product.query.get(product_id):
            raise ValueError(f"There is no product with id {product_id}")
        return product_id


# ChatMessage model represents a chat message.
class ChatMessage(db.Model, SerializerMixin):
    __tablename__ = "chat_messages"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_auth.id"), nullable=False)
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("UserAuth", back_populates="chat_messages")
    serialize_rules = ("-user.chat_messages",)


# AITrainingData model represents AI training data.
class AITrainingData(db.Model, SerializerMixin):
    __tablename__ = "ai_training_data"
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class OpenAIInteraction(db.Model, SerializerMixin):
    __tablename__ = "openai_interactions"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_auth.id"), nullable=True)
    request_data = db.Column(db.Text, nullable=False)  # JSON data sent to OpenAI
    response_data = db.Column(db.Text, nullable=False)  # JSON response from OpenAI
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("UserAuth", back_populates="openai_interactions")


UserAuth.openai_interactions = db.relationship(
    "OpenAIInteraction", back_populates="user"
)
