import json

# import sys
from random import randint

from utils import get_http, post_http

URL = "http://localhost:8000/api"


def create_user_address(token, data):
    headers = {"Content-Type": "application/json", "Authorization": "Token " + token}
    user_detail_url = URL + "/users/address/"
    post_http(headers, user_detail_url, json.dumps(data))


def list_user_address(token):
    headers = {"Content-Type": "application/json", "Authorization": "Token " + token}
    user_detail_url = URL + "/users/address/"
    resp = get_http(headers, user_detail_url)
    return resp


def main():
    user_data = {}
    poll_address = []
    with open("api_functional_test/user_login_data.json") as f:
        user_data = json.load(f)
    with open("api_functional_test/poll_address.json") as f:
        poll_address = json.load(f)

    for key, user in user_data.items():
        token = user["token"]
        for i in range(0, randint(1, 3)):
            address = poll_address[randint(0, len(poll_address) - 1)]
            address["default"] = True if i == 0 else False
            create_user_address(token, address)


if __name__ == "__main__":
    main()
