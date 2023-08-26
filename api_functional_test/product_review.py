import json
import sys
from random import randint

from utils import get_http, post_http

URL = "http://localhost:8000/api"

NUM_REVIEWS_PER_USER = 10
if len(sys.argv) > 1:
    NUM_REVIEWS_PER_USER = int(sys.argv[1])


def list_reviews(url):
    header = {"Content-Type": "application/json"}

    res = get_http(header, url, verbose=True)
    return res


def create_review(url, data, token):
    header = {"Content-Type": "application/json", "Authorization": "Token " + token}

    res = post_http(header, url, json.dumps(data), verbose=True)
    return res


def main():
    user_data = {}
    with open("api_functional_test/user_login_data.json") as f:
        user_data = json.load(f)

    url = URL + "/wines/3/reviews/"
    res = list_reviews(url)
    print(res)

    num_users = 1  # randint(1, len(user_data))
    keys = list(user_data.keys())
    users = keys[:num_users]
    for username in users:
        token = user_data[username]["token"]
        for _ in range(NUM_REVIEWS_PER_USER):
            product_id = randint(1, 100)
            url = URL + f"/wines/{product_id}/reviews/"
            data = {"review": "This is a test review", "rating": randint(1, 5)}
            res = create_review(url, data, token)
            print(res)


if __name__ == "__main__":
    main()
