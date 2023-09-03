import json

from login import login
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


def logout(token):
    header = {"Content-Type": "application/json", "Authorization": f"Token {token}"}
    url = f"{URL}/users/auth/logout/"
    response = post_http(header, url, json.dumps({}), verbose=True)
    return response


def main():
    user_data = {}
    with open("api_functional_test/poll_users_data.json") as f:
        user_data = json.load(f)
    username = "smelloy2m"
    password = [user_data[i]["password"] for i in range(len(user_data)) if user_data[i]["username"] == username][0]
    token = login(username, password)
    # cart = get_card(token)
    data = {"product": 1, "quantity": 64}
    add_item(token, data)
    logout(token)
    # items_ids = [randint(1, 100) for _ in range(5)]
    # for item_id in items_ids:
    #     data = {"product": item_id, "quantity": randint(1, 10)}
    #     add_item(token, data)


if __name__ == "__main__":
    main()
