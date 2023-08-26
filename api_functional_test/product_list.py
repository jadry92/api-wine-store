import sys

from utils import get_http

URL = "http://localhost:8000/api"

ID = None
print(sys.argv)
if len(sys.argv) > 1:
    ID = int(sys.argv[1])


def list_products(url):
    headers = {"Content-Type": "application/json"}
    data = get_http(headers, url)
    print(data)


def main():
    if ID is None:
        list_products(URL + "/wines/")
    else:
        list_products(URL + f"/wines/{ID}/")


if __name__ == "__main__":
    main()
