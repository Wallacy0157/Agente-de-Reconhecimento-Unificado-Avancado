import requests
from requests import Response

BASE_URL = "http://localhost:8080"

session = requests.Session()
session.headers.update({"Content-Type": "application/json"})


def post(endpoint: str, payload: dict) -> Response:
    return session.post(f"{BASE_URL}{endpoint}", json=payload)


def get(endpoint: str, **kwargs) -> Response:
    return session.get(f"{BASE_URL}{endpoint}", **kwargs)
