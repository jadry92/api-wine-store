import hashlib
import json
import random

from utils import get_http, post_http


def question(question, options):
    flag = True
    while flag:
        option = input(question)
        if option in options:
            flag = False
        else:
            print(f"Sorry select one of option {options}")
    return option


def setup_options():
    options = {
        "verbose": None,
        "number_of_users": 1,
    }
    answer = question("Do you want to see the verbose? (y/n): ", ["y", "n"])
    if answer == "y":
        options["verbose"] = True
    else:
        options["verbose"] = False

    answer = question("How many users do you want to create? (1-100): ", [str(i) for i in range(1, 101)])
    options["number_of_users"] = int(answer)

    return options


def login_users(URLs, poll_user_data, options):
    users_data = {}
    users = random.choices(poll_user_data, k=options["number_of_users"])
    url = URLs["login"]
    for user in users:
        data = {"username": user["username"], "password": user["password"]}
        headers = {"Content-Type": "application/json"}
        response = post_http(headers, url, json.dumps(data), verbose=True)
        token = response.get("key")
        users_data[user["username"]] = {"username": user["username"], "token": token}

    return users_data


def add_wines_to_cart(URLs, users, options):
    cart_data = []
    headers = {
        "Content-Type": "application/json",
    }
    pages = 5
    all_wines = []
    print("Getting all wines")
    for page in range(1, pages + 1):
        raw = get_http(headers, URLs["wines"] + f"?page={page}", verbose=False)
        all_wines.extend(raw["results"])

    for _, user in users.items():
        headers = {"Content-Type": "application/json", "Authorization": f"Token {user['token']}"}

        print(f"Adding items to {user['username']}'s cart")
        url = URLs["cart_item"]
        wines = random.sample(all_wines, k=random.randint(1, 10))
        for wine in wines:
            data = {"product": wine["id"], "quantity": random.randint(1, 10)}
            post_http(headers, url, json.dumps(data), verbose=options["verbose"])
            cart_data.append(data)
        print(f"${len(wines)} items added to {user['username']}'s cart")

    return cart_data


def add_address_to_user(URLs, token, options, address):
    headers = {"Content-Type": "application/json", "Authorization": f"Token {token}"}
    url = URLs["user_address"]
    address = post_http(headers, url, json.dumps(address), verbose=options["verbose"])

    return address["id"]


def add_payment_to_user(URLs, token, options, username):
    PROVIDERS = ["square", "paypal", "stripe", "payoneer", "paytm", "payu", "payza", "payeer", "payone", "payza"]
    provider = PROVIDERS[random.randint(0, len(PROVIDERS) - 1)]
    blop = username + provider + str(random.randint(0, 1000000))
    payment = {
        "payment_method": hashlib.sha256(blop.encode()).hexdigest(),
        "provider": provider,
    }
    headers = {"Content-Type": "application/json", "Authorization": f"Token {token}"}
    url = URLs["user_payment"]
    payment = post_http(headers, url, json.dumps(payment), verbose=options["verbose"])

    return payment["id"]


def place_order(URLs, users, options, poll_address_data):
    for username, user in users.items():
        print(f"Placing order for {user['username']}")
        headers = {"Content-Type": "application/json", "Authorization": f"Token {user['token']}"}
        print(f"Getting {user['username']}'s shipping address and payment method")
        resp = get_http(headers, URLs["user_address"], verbose=options["verbose"])
        address_id = None
        for address in resp:
            if address["default"]:
                address_id = address["id"]
                break
        if address_id is None:
            print("No default address found, adding one")
            address = random.choice(poll_address_data)
            address_id = add_address_to_user(URLs, user["token"], options, address)

        print("here-", headers)
        resp = get_http(headers, URLs["user_payment"], verbose=options["verbose"])
        payment_id = None
        for payment in resp:
            if payment["default"]:
                payment_id = payment["id"]
                break
        if payment_id is None:
            print("No default payment found, adding one")
            payment_id = add_payment_to_user(URLs, user["token"], options, username)

        data = {"shipping_address": address_id, "payment_method_id": payment_id}

        res = post_http(headers, URLs["order"], json.dumps(data), verbose=options["verbose"])
        print(f"Order placed for {user['username']}")
        print(res)

    return None


def get_order_detail(URLs, users, options):
    for username, user in users.items():
        headers = {"Content-Type": "application/json", "Authorization": f"Token {user['token']}"}
        resp = get_http(headers, URLs["order"], verbose=options["verbose"])
        print(resp)


def walkthrough_store(URLs, poll_user_data, poll_address_data):
    options = setup_options()
    print(f"By default the app has 100 user registered, we will use the first {options['number_of_users']} users")
    print("We don't test registration because we need to confirm the email to be available to login")
    print("The first step is to login with the user")
    users = login_users(URLs, poll_user_data, options)
    print("The second step is to add wines to the cart")
    add_wines_to_cart(URLs, users, options)
    print("The third step is to place the order")
    place_order(URLs, users, options, poll_address_data)
    print("The fifth step is to get the order detail")
    get_order_detail(URLs, users, options)
