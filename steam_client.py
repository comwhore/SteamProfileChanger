import requests

from config import (
    SESSION_ID,
    STEAM_LOGIN_SECURE,
)

session = requests.Session()

session.cookies.set(
    "sessionid",
    SESSION_ID,
    domain="steamcommunity.com"
)

session.cookies.set(
    "steamLoginSecure",
    STEAM_LOGIN_SECURE,
    domain="steamcommunity.com"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/136.0.0.0 Safari/537.36"
    ),
    "Origin": "https://steamcommunity.com",
    "Referer": "https://steamcommunity.com/"
}