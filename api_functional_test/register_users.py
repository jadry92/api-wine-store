# Utils
import json
import time

from utils import post_http

URL = "http://localhost:8000/api"


def register_user(username, email, password, first_name, last_name):
    register_url = f"{URL}/users/auth/registration/"
    data = {
        "username": username,
        "email": email,
        "password1": password,
        "password2": password,
        "first_name": first_name,
        "last_name": last_name,
    }
    headers = {"Content-Type": "application/json"}
    response = post_http(headers, register_url, json.dumps(data))
    return response


def main():
    with open("api_functional_test/user_data.json") as f:
        users = json.load(f)
        for user in users:
            register_user(
                user.get("username"),
                user.get("email"),
                user.get("password"),
                user.get("first_name"),
                user.get("last_name"),
            )
            time.sleep(1)


if __name__ == "__main__":
    main()
