import json

from utils import get_http, post_http

# from random import randint


URL = "http://localhost:8000/api/"


def create_order(token, data):
    """Create order."""
    url = URL + "orders/"
    headers = {"Content-Type": "application/json", "Authorization": f"Token {token}"}
    response = post_http(url, headers, json.dumps(data), verbose=True)
    return response


def get_orders(token):
    """Get Orders"""
    url = URL + "orders/"
    headers = {"Content-Type": "application/json", "Authorization": f"Token {token}"}
    response = get_http(url, headers, verbose=True)
    return response


def main():
    user_data = {}
    with open("api_functional_test/user_login_data.json") as file:
        user_data = json.load(file)

    list(user_data.keys())
    token = user_data["tgibbetts0"]["token"]

    data = {"shipping_address": 1, "payment_method_id": 1}

    create_order(token, data)


if __name__ == "__main__":
    main()
