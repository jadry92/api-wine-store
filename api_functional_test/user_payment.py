import hashlib
import json
from random import randint

from utils import get_http, post_http

URL = "http://localhost:8000/api"

PROVIDERS = ["square", "paypal", "stripe", "payoneer", "paytm", "payu", "payza", "payeer", "payone", "payza"]


def create_payment_method(data, token):
    header = {"Content-Type": "application/json", "Authorization": "Token " + token}
    url = URL + "/users/payment/"

    res = post_http(header, url, json.dumps(data), verbose=True)
    return res


def main():
    user_data = {}
    with open("api_functional_test/user_login_data.json") as f:
        user_data = json.load(f)

    for username in user_data.keys():
        number_ot_payment_methods = randint(1, 5)
        for i in range(number_ot_payment_methods):
            provider = PROVIDERS[randint(0, len(PROVIDERS) - 1)]
            blop = username + provider + str(randint(0, 1000000))
            data = {
                "payment_method": hashlib.sha256(blop.encode()).hexdigest(),
                "provider": provider,
                "default": True if i == 0 else False,
            }
            create_payment_method(data, user_data[username]["token"])


if __name__ == "__main__":
    # main()
    token = "a1d58517e93b0ed316ef2b47a74bfe984654aff8"
    header = {"Content-Type": "application/json", "Authorization": "Token " + token}
    res = get_http(header, "http://localhost:8000/api/users/payment/", verbose=True)
    username = "ndrewett1s"
    provider = PROVIDERS[randint(0, len(PROVIDERS) - 1)]
    blop = username + provider + str(randint(0, 1000000))
    data = {
        "payment_method": hashlib.sha256(blop.encode()).hexdigest(),
        "provider": provider,
        "default": True,
    }
    if len(res) == 0:
        create_payment_method(data, token)
