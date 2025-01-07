import requests


def perform_request(url, method, headers):
    return requests.request(method, url, headers=headers)