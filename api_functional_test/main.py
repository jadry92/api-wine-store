"""
This file is for testing api.
    Options:
        1. Walkthrough Full Store Logic
        2. Walkthrough User Logic
        3. Walkthrough Cart-Order Logic
        4. Walkthrough Products Logic
        5. Exit
"""
# Lib
import json

# Local
from walk_store import walkthrough_store

BASE_URL = "http://127.0.0.1:8000/api/"

URLs = {
    "register": BASE_URL + "users/auth/registration/",
    "login": BASE_URL + "users/auth/login/",
    "user_detail": BASE_URL + "users/auth/user/",
    "user_address": BASE_URL + "users/address/",
    "user_payment": BASE_URL + "users/payment/",
    "logout": BASE_URL + "users/auth/logout/",
    "wines": BASE_URL + "wines/",
    "wine_detail": lambda wine_id: BASE_URL + f"wines/{wine_id}/",
    "cart": BASE_URL + "cart/",
    "cart_detail": lambda cart_id: BASE_URL + f"cart/{cart_id}/",
    "cart_item": BASE_URL + "cart/items/",
    "order": BASE_URL + "orders/",
}

data_files = {
    "users_data": "api_functional_test/poll_users_data.json",
    "address": "api_functional_test/poll_address.json",
}


def main():
    user_data = []
    address_data = []
    with open(data_files["users_data"]) as f:
        user_data = json.load(f)

    with open(data_files["address"]) as f:
        address_data = json.load(f)

    flag_while = True
    while flag_while:
        print("Please select the option")
        print("1. Walkthrough Full Store Logic")
        print("2. Walkthrough User Logic")
        print("3. Walkthrough Cart-Order Logic")
        print("4. Walkthrough Products Logic")
        print("5 Exit")
        option = input("Enter the option: ")
        if option == "1":
            walkthrough_store(URLs, user_data, address_data)
        elif option == "2":
            pass
        elif option == "3":
            pass
        elif option == "4":
            pass
        elif option == "5":
            flag_while = False
        else:
            print("Please select the correct option")


if __name__ == "__main__":
    main()
