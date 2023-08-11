import requests

URL = "http://localhost:8000"


def get(url):
    print(f"GET {url}")
    response = requests.get(url)
    print(f"{response.status_code}")
    return response


print(get(URL + "/api/wines/").json())
