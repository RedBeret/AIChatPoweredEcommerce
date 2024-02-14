#!/usr/bin/env python3

# Standard library imports
import random
import uuid
from datetime import datetime

# Local imports
from app import app, db

# Remote library imports
from faker import Faker
from flask_bcrypt import Bcrypt
from models import (
    AITrainingData,
    ChatMessage,
    Color,
    Order,
    OrderDetail,
    Product,
    ProductColor,
    ShippingInfo,
    UserAuth,
    UserSession,
)

# Instantiate Faker
fake = Faker()

# Setup bcrypt
bcrypt = Bcrypt(app)


def seed_database():
    with app.app_context():
        # Drop all tables and recreate them
        db.drop_all()
        db.create_all()

        # Create fake data for UserAuth
        user_ids = []  # Keep track of user IDs for later use
        for _ in range(3):
            password_hash = bcrypt.generate_password_hash("123456").decode("utf-8")
            user = UserAuth(
                username=fake.user_name(),
                email=fake.email(),
                password_hash=password_hash,
            )
            db.session.add(user)
            db.session.flush()  # Flush to assign an ID to the user object
            user_ids.append(user.id)

        db.session.commit()

        for user_id in user_ids:
            user_session = UserSession(
                user_id=user_id,
                started_at=fake.date_time_between(start_date="-1y", end_date="now"),
                ended_at=(
                    fake.date_time_between(start_date="-1y", end_date="now")
                    if random.choice([True, False])
                    else None
                ),
            )
            db.session.add(user_session)

        db.session.commit()

        product_ids = []
        product_names = ["Vision X Pro Max Ultra", "Halo Vision Pro Ultra"]
        product_descriptions = [
            "The Vision X Pro Max Ultra represents the pinnacle of smartphone technology, boasting a transparent design that reveals the cutting-edge tech within. Featuring a modular build for easy upgrades and repairs, it sets a new standard for innovation and sustainability in the mobile industry.",
            "The New Halo Vision Pro Ultra is the latest in our line of cutting-edge smartphones, offering unparalleled performance and design. With its sleek build and advanced features, it's designed to push the boundaries of what a smartphone can do.",
        ]
        product_prices = [100000, 150000]
        product_images = ["img/visionxphone.png", "img/visionxhalo.png"]
        product_image_alts = ["Vision X Pro Max Ultra", "Halo Vision Pro Ultra"]

        for i in range(len(product_names)):
            product = Product(
                name=product_names[i],
                description=product_descriptions[i],
                item_quantity=100,
                price=product_prices[i],
                image_path=product_images[i],
                imageAlt=product_image_alts[i],
            )
            db.session.add(product)
            db.session.flush()
            product_ids.append(product.id)
        db.session.commit()

        # Create fake data for Colors
        color_ids = []
        colors = ["Black", "Transparent"]
        for color_name in colors:
            color = Color(name=color_name)
            db.session.add(color)
            db.session.flush()
            color_ids.append(color.id)

        db.session.commit()

        # Create fake data for ProductColor relationships
        for product_id in product_ids:
            for color_id in color_ids:
                # Assign each color to each product
                product_color = ProductColor(product_id=product_id, color_id=color_id)
                db.session.add(product_color)

        db.session.commit()

        # Create fake data for ShippingInfo
        for _ in range(3):
            shipping_info = ShippingInfo(
                address_line1=fake.street_address(),
                address_line2=fake.secondary_address(),
                city=fake.city(),
                state=fake.state(),
                postal_code=fake.zipcode(),
                country=fake.country(),
                phone_number=fake.phone_number(),
            )
            db.session.add(shipping_info)
        db.session.commit()

        # Create fake data for Orders and OrderDetails
        for _ in range(2):
            order = Order(
                user_id=random.choice(user_ids),
                shipping_info_id=random.choice(user_ids),
                confirmation_num=str(uuid.uuid4()),
            )
            db.session.add(order)
            db.session.flush()

            for _ in range(random.randint(1, 5)):
                order_detail = OrderDetail(
                    order_id=order.id,
                    product_id=random.choice(product_ids),
                    quantity=random.randint(1, 3),
                    color_id=random.choice(color_ids),
                )
                db.session.add(order_detail)

        db.session.commit()

        # Create fake data for ChatMessages
        for _ in range(0):
            chat_message = ChatMessage(
                user_id=random.choice(user_ids),
                message=fake.sentence(),
                response=fake.sentence(),
                timestamp=datetime.utcnow(),
            )
            db.session.add(chat_message)

        db.session.commit()

        # Create fake data for AITrainingData
        for _ in range(10):
            ai_data = AITrainingData(data=fake.text(max_nb_chars=200))
            db.session.add(ai_data)

        db.session.commit()

        print("Database seeded successfully!")


if __name__ == "__main__":
    seed_database()
