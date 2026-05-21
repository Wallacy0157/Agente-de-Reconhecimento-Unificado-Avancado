import requests
from requests import Response

BASE_URL = "http://localhost:8080"
PUBLIC_ENDPOINTS = {"/usuarios", "/usuarios/login"}

session = requests.Session()
session.headers.update({"Content-Type": "application/json"})


def set_token(token: str) -> None:
    session.headers.update({"Authorization": f"Bearer {token}"})


def _request(method: str, endpoint: str, **kwargs) -> Response:
    if endpoint in PUBLIC_ENDPOINTS:
        headers = kwargs.pop("headers", {})
        headers.pop("Authorization", None)
        kwargs["headers"] = headers
    return session.request(method, f"{BASE_URL}{endpoint}", **kwargs)


def post(endpoint: str, payload: dict) -> Response:
    return _request("POST", endpoint, json=payload)


def get(endpoint: str, **kwargs) -> Response:
    return _request("GET", endpoint, **kwargs)
