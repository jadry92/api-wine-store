import json
from random import randint

from utils import get_http, post_http

URL = "http://localhost:8000/api"


def get_card(token):
    header = {"Content-Type": "application/json", "Authorization": f"Token {token}"}
    url = f"{URL}/cart/"
    response = get_http(header, url, verbose=True)
    return response


def add_item(token, data):
    header = {"Content-Type": "application/json", "Authorization": f"Token {token}"}
    url = f"{URL}/cart/items/"
    response = post_http(header, url, json.dumps(data), verbose=True)
    return response


def get_items(token):
    header = {"Content-Type": "application/json", "Authorization": f"Token {token}"}
    url = f"{URL}/cart/items/"
    response = get_http(header, url, verbose=True)
    return response


def main():
    user_data = {}
    with open("api_functional_test/user_login_data.json") as f:
        user_data = json.load(f)

    keys = list(user_data.keys())
    token = user_data[keys[randint(0, len(keys) - 1)]]["token"]
    get_card(token)
    get_items(token)
    items_ids = [randint(1, 100) for _ in range(5)]
    for item_id in items_ids:
        data = {"product": item_id, "quantity": randint(1, 10)}
        add_item(token, data)


if __name__ == "__main__":
    main()
