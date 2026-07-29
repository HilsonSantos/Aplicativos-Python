"""Cliente HTTP simples para a API do APPVET, usado pelas páginas do Streamlit."""

import os

import requests

API_URL = os.getenv("APPVET_API_URL", "http://localhost:8000")


def get(path: str, params: dict | None = None):
    resp = requests.get(f"{API_URL}{path}", params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()


def post(path: str, json: dict):
    resp = requests.post(f"{API_URL}{path}", json=json, timeout=10)
    resp.raise_for_status()
    return resp.json()


def patch(path: str, json: dict | None = None, params: dict | None = None):
    resp = requests.patch(f"{API_URL}{path}", json=json, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()


def delete(path: str):
    resp = requests.delete(f"{API_URL}{path}", timeout=10)
    resp.raise_for_status()
