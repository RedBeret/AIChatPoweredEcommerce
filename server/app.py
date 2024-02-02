#!/usr/bin/env python3

# Standard library imports
import os

# Local imports
from config import create_app, init_extensions

# from dotenv import load_dotenv
from flask import make_response, request
from flask_jwt_extended import create_access_token, jwt_required
from flask_restful import Resource
from marshmallow import fields, validate
from models import ChatMessage, Color, Order, Product, ShippingInfo, UserAuth


app = create_app()
db, ma, bcrypt, jwt, api = init_extensions(app)


@app.route("/")
def index():
    return "<h1>ChatPoweredEcommerce</h1>"


# User Authentication Resource
class UserAuthResource(Resource):
    def get(self):
        return make_response([user.to_dict() for user in UserAuth.query.all()], 200)

    def post(self):
        user_data = request.get_json()
        # Checks if user already exists
        if UserAuth.query.filter_by(username=user_data["username"]).first():
            return make_response({"error": "Username already exists."}, 400)

        # Creates a new user
        try:
            new_user = UserAuth(
                username=user_data["username"],
                email=user_data["email"],
            )
            new_user.password = user_data["password"]
            db.session.add(new_user)
            db.session.commit()
            return make_response({"message": "User created successfully"}, 201)
        except Exception as error:
            db.session.rollback()
            return make_response({"error": str(error)}, 500)

    def delete(self):
        data = request.get_json()
        user = UserAuth.query.filter_by(username=data["username"]).first()
        if user and user.check_password(data["password"]):
            db.session.delete(user)
            db.session.commit()
            return make_response({"message": "User deleted successfully"}, 200)
        else:
            return make_response({"error": "Invalid credentials"}, 401)

    def patch(self):
        data = request.get_json()
        user = UserAuth.query.filter_by(username=data["username"]).first()
        if user and user.check_password(data["password"]):
            user.password = data["newPassword"]
            db.session.commit()
            return make_response({"message": "Password updated successfully"}, 200)
        else:
            return make_response({"error": "Invalid credentials"}, 401)


class UserLoginResource(Resource):
    def post(self):
        data = request.get_json()
        user = UserAuth.query.filter_by(username=data["username"]).first()
        if user and user.check_password(data["password"]):
            access_token = create_access_token(identity=user.id)
            return {"access_token": access_token}, 200
        return {"message": "Invalid credentials"}, 401


# ShippingInfo Resource
class ShippingInfoResource(Resource):
    @jwt_required()
    def get(self, user_id):
        user = UserAuth.query.get(user_id)
        if user and user.shipping_info:
            return make_response(user.shipping_info.to_dict(), 200)
        return make_response({"message": "Shipping info not found"}, 404)

    @jwt_required()
    def post(self, user_id):
        user = UserAuth.query.get(user_id)
        if not user:
            return make_response({"error": "User not found"}, 404)

        shipping_data = request.get_json()
        shipping_info = ShippingInfo(
            user_id=user_id,
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
        return make_response({"message": "Shipping info added successfully"}, 201)

    @jwt_required()
    def patch(self, user_id):
        user = UserAuth.query.get(user_id)
        if not user or not user.shipping_info:
            return make_response({"error": "Shipping info not found"}, 404)

        shipping_data = request.get_json()
        shipping_info = user.shipping_info
        shipping_info.address_line1 = shipping_data.get(
            "address_line1", shipping_info.address_line1
        )
        shipping_info.address_line2 = shipping_data.get(
            "address_line2", shipping_info.address_line2
        )
        shipping_info.city = shipping_data.get("city", shipping_info.city)
        shipping_info.state = shipping_data.get("state", shipping_info.state)
        shipping_info.postal_code = shipping_data.get(
            "postal_code", shipping_info.postal_code
        )
        shipping_info.country = shipping_data.get("country", shipping_info.country)
        shipping_info.phone_number = shipping_data.get(
            "phone_number", shipping_info.phone_number
        )

        db.session.commit()
        return make_response({"message": "Shipping info updated successfully"}, 200)


# Product Resource
class ProductResource(Resource):
    @jwt_required()
    def get(self, product_id=None):
        if product_id:
            product = Product.query.get(product_id)
            if product:
                return make_response(ProductSchema().dump(product), 200)
            return make_response({"error": "Product not found"}, 404)
        else:
            products = Product.query.all()
            return make_response(ProductSchema(many=True).dump(products), 200)

    @jwt_required()
    def post(self):
        product_data = request.get_json()
        new_product = Product(
            name=product_data["name"],
            description=product_data.get("description", ""),
            price=product_data["price"],
            image_path=product_data.get("image_path", ""),
            imageAlt=product_data.get("imageAlt", ""),
        )

        db.session.add(new_product)
        db.session.commit()
        return make_response({"message": "Product created successfully"}, 201)

    @jwt_required()
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

    @jwt_required()
    def delete(self, product_id):
        product = Product.query.get(product_id)
        if not product:
            return make_response({"error": "Product not found"}, 404)

        db.session.delete(product)
        db.session.commit()
        return make_response({"message": "Product deleted successfully"}, 200)


class UserAuthSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserAuth
        load_instance = True
        exclude = ("password_hash",)

    password = fields.Str(
        load_only=True, required=True, validate=validate.Length(min=6)
    )


# Product Schema
class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True


# Color Resource
class ColorResource(Resource):
    @jwt_required()
    def get(self, color_id):
        color = Color.query.get(color_id)
        pass


# ChatMessage Resource
class ChatMessageResource(Resource):
    @jwt_required()
    def get(self, message_id):
        message = ChatMessage.query.get(message_id)
        pass


# Order Resource
class OrderResource(Resource):
    @jwt_required()
    def get(self, order_id):
        order = Order.query.get(order_id)
        pass


# Routing
api.add_resource(UserLoginResource, "/login")
api.add_resource(UserAuthResource, "/user_auth")
api.add_resource(ShippingInfoResource, "/user/<int:user_id>/shipping_info")
api.add_resource(ProductResource, "/product", "/product/<int:product_id>")
api.add_resource(ColorResource, "/color/<int:color_id>")
api.add_resource(ChatMessageResource, "/chat_message/<int:message_id>")
api.add_resource(OrderResource, "/order/<int:order_id>")


if __name__ == "__main__":
    app.run(port=5555, debug=True)
