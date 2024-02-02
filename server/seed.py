#!/usr/bin/env python3

# Standard library imports
import random
from random import choice as rc
from random import randint

# Local imports
from app import app, db

# Remote library imports
from faker import Faker
from models import (
    AITrainingData,
    ChatMessage,
    Color,
    OpenAIInteraction,
    Order,
    Product,
    UserAuth,
    db,
)

fake = Faker()


def create_users(n=10):
    """Create N fake users"""
    for _ in range(n):
        user = UserAuth(
            username=faker.user_name(),
            email=faker.email(),
            password_hash=faker.password(),
        )
        db.session.add(user)
    db.session.commit()


def create_products(n=5):
    """Create N fake products"""
    for _ in range(n):
        product = Product(
            name=faker.word(),
            description=faker.text(),
            price=random.randint(100, 10000),  # price in cents
        )
        db.session.add(product)
    db.session.commit()


def create_colors(n=3):
    """Create N fake colors"""
    colors = ["Red", "Blue", "Green", "Yellow", "Black", "White"]
    for _ in range(n):
        color = Color(name=random.choice(colors))
        db.session.add(color)
        colors.remove(color.name)
    db.session.commit()


def create_orders(n=5):
    """Create N fake orders"""
    users = UserAuth.query.all()
    products = Product.query.all()
    for _ in range(n):
        order = Order(
            user_id=random.choice(users).id, created_at=faker.date_time_this_year()
        )
        db.session.add(order)
    db.session.commit()


def create_chat_messages(n=20):
    """Create N fake chat messages"""
    users = UserAuth.query.all()
    for _ in range(n):
        chat_message = ChatMessage(
            user_id=random.choice(users).id,
            message=faker.sentence(),
            response=faker.sentence(),
            timestamp=faker.date_time_this_year(),
        )
        db.session.add(chat_message)
    db.session.commit()


def create_ai_interactions(n=10):
    """Create N fake AI interactions"""
    users = UserAuth.query.all()
    for _ in range(n):
        interaction = OpenAIInteraction(
            user_id=random.choice(users).id,
            request_data=faker.sentence(),
            response_data=faker.sentence(),
            created_at=faker.date_time_this_year(),
        )
        db.session.add(interaction)
    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        print("Starting seed process...")

        db.drop_all()
        db.create_all()

        create_users()
        create_products()
        create_colors()
        create_orders()
        create_chat_messages()
        create_ai_interactions()

        print("Database seeded successfully.")
