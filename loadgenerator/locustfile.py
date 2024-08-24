#!/usr/bin/python
import random
from locust import FastHttpUser, TaskSet, between
from faker import Faker
import datetime

fake = Faker()

products = [
    "0PUK6V6EV0",
    "1YMWWN1N4O",
    "2ZYFJ3GM2N",
    "66VCHSJNUP",
    "6E92ZMYYFZ",
    "9SIQT8TOJO",
    "L9ECAV7KIM",
    "LS4PSXUNUM",
    "OLJCESPC7Z",
]


def index(l):
    """Handles the GET request to the index page."""
    l.client.get("/")


def setCurrency(l):
    """Handles the POST request to set the currency, randomly choosing one from a list."""
    currencies = ["EUR", "USD", "JPY", "CAD", "GBP", "TRY"]
    l.client.post("/setCurrency", {"currency_code": random.choice(currencies)})


def browseProduct(l):
    """Handles the GET request to view a product, randomly choosing one from a list."""
    l.client.get("/product/" + random.choice(products))


def viewCart(l):
    """Handles the GET request to view the cart."""
    l.client.get("/cart")


def addToCart(l):
    """Handles the GET request to view a product and the POST request to add that product to the cart."""
    product = random.choice(products)
    l.client.get("/product/" + product)
    l.client.post("/cart", {"product_id": product, "quantity": random.randint(1, 10)})


def empty_cart(l):
    """Handles the POST request to empty the cart."""
    l.client.post("/cart/empty")


def checkout(l):
    """Handles the POST request to add a product to the cart and the POST request to checkout."""
    addToCart(l)
    current_year = datetime.datetime.now().year + 1
    l.client.post(
        "/cart/checkout",
        {
            "email": fake.email(),
            "street_address": fake.street_address(),
            "zip_code": fake.zipcode(),
            "city": fake.city(),
            "state": fake.state_abbr(),
            "country": fake.country(),
            "credit_card_number": fake.credit_card_number(card_type="visa"),
            "credit_card_expiration_month": random.randint(1, 12),
            "credit_card_expiration_year": random.randint(
                current_year, current_year + 70
            ),
            "credit_card_cvv": f"{random.randint(100, 999)}",
        },
    )


def logout(l):
    l.client.get("/logout")


class UserBehavior(TaskSet):

    def on_start(self):
        index(self)

    tasks = {
        index: 1,
        setCurrency: 2,
        browseProduct: 10,
        addToCart: 2,
        viewCart: 3,
        checkout: 1,
    }


class WebsiteUser(FastHttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 10)
