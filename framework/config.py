import os

from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://jsonplaceholder.typicode.com")
TIMEOUT_MS = float(os.getenv("API_TIMEOUT_MS", "15000"))
API_TOKEN = os.getenv("API_TOKEN", "")
# Which HTTP backend(s) to run tests with: playwright, requests, or both
API_CLIENT = os.getenv("API_CLIENT", "both").lower()
CLIENTS = ["playwright", "requests"] if API_CLIENT == "both" else [API_CLIENT]


def default_headers() -> dict:
    headers = {"Accept": "application/json"}
    if API_TOKEN:
        headers["Authorization"] = f"Bearer {API_TOKEN}"
    return headers
