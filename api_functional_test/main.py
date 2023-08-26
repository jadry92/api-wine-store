import json

from utils import get_http, post_http

URL = "http://localhost:8000/api"


if __name__ == "__main__":
    # register flow
    register_url = URL + "/users/auth/registration/"
    num = 40
    data = {
        "username": f"test{num}",
        "email": f"test_{num}@exmaple.com",
        "first_name": f"test_{num}",
        "last_name": f"test_last_{num}",
        "password1": "Tdjsagdjhgasjd_123123",
        "password2": "Tdjsagdjhgasjd_123123",
    }
    headers = {"Content-Type": "application/json"}
    post_http(headers, register_url, json.dumps(data))
    # login flow
    login_url = URL + "/users/auth/login/"
    data = {"username": "test_2", "password": "Tdjsagdjhgasjd_123123"}
    res = post_http(headers, login_url, json.dumps(data))
    token = res.get("key")
    if token is None:
        raise Exception("token is None")
    # user detail flow
    headers = {"Content-Type": "application/json", "Authorization": "Token " + token}
    user_detail_url = URL + "/users/auth/user/"
    data = {}
    get_http(headers, user_detail_url, json.dumps(data))

    # logout flow
    logout_url = URL + "/users/auth/logout/"
    data = {}
    post_http(headers, logout_url, json.dumps(data))

    headers = {"Content-Type": "application/json", "Authorization": "Token " + token}
    user_detail_url = URL + "/users/auth/user/"
    data = {}
    get_http(headers, user_detail_url, json.dumps(data))
