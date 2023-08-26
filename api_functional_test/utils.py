import requests


def get_http(header, url, verbose=False):
    response = requests.get(url, headers=header)
    if verbose:
        print(f" CODE : {response.status_code}")
    if response.status_code == 500:
        print(f"server error {url}")
        print(response.content)
        exit(1)

    if hasattr(response, "json"):
        if verbose:
            print(response.json())
        return response.json()
    else:
        if verbose:
            print(response.content)


def post_http(header, url, data, verbose=False):
    response = requests.post(url, headers=header, data=data)
    if verbose:
        print(f" CODE : {response.status_code}")

    if response.status_code == 500:
        print(f"server error {url}")
        print(response.content)
        exit(1)

    if hasattr(response, "json"):
        if verbose:
            print(response.json())
        return response.json()
    else:
        if verbose:
            print(response.content)


def put_http(header, url, data, verbose=False):
    response = requests.put(url, headers=header, data=data)
    if verbose:
        print(f" CODE : {response.status_code}")

    if response.status_code == 500:
        print(f"server error {url}")
        print(response.content)
        exit(1)

    if hasattr(response, "json"):
        if verbose:
            print(response.json())
        return response.json()
    else:
        if verbose:
            print(response.content)


def path_http(header, url, data, verbose=False):
    response = requests.patch(url, headers=header, data=data)
    if verbose:
        print(f" CODE : {response.status_code}")

    if response.status_code == 500:
        print(f"server error {url}")
        print(response.content)
        exit(1)

    if hasattr(response, "json"):
        if verbose:
            print(response.json())
        return response.json()
    else:
        if verbose:
            print(response.content)


def delete_http(header, url, verbose=False):
    response = requests.delete(url, headers=header)
    if verbose:
        print(f" CODE : {response.status_code}")

    if response.status_code == 500:
        print(f"server error {url}")
        print(response.content)
        exit(1)

    if hasattr(response, "json"):
        if verbose:
            print(response.json())
        return response.json()
    else:
        if verbose:
            print(response.content)
