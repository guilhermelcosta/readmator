import requests


def perform_request(url, method, token, body=None):
    return requests.request(method, url, headers=_create_headers(token), json=body)


def _create_headers(token):
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
