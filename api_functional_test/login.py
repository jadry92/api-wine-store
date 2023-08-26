import json
import sys

from utils import post_http

URL = "http://localhost:8000/api"

NUMBER_LOGIN = 10
if len(sys.argv) > 2:
    num = int(sys.argv[2])
    if num > 0 and num <= 100:
        NUMBER_LOGIN = num


def login(username, password):
    login_url = f"{URL}/users/auth/login/"
    data = {"username": username, "password": password}
    headers = {"Content-Type": "application/json"}
    response = post_http(headers, login_url, json.dumps(data))
    return response.get("key")


if __name__ == "__main__":
    user_data = {}
    with open("api_functional_test/user_data.json") as f:
        data = json.load(f)
        for i in range(0, NUMBER_LOGIN):
            user_data[data[i]["username"]] = {"username": data[i].get("username"), "password": data[i].get("password")}

    for key, user in user_data.items():
        token = login(user["username"], user["password"])
        if token is None:
            raise Exception("token is None")
        user_data[key]["token"] = token

    with open("api_functional_test/user_login_data.json", "w") as f:
        json.dump(user_data, f)
