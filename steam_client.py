import requests

from session_loader import load_session_credentials

session = requests.Session()

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/136.0.0.0 Safari/537.36"
    ),
    "Origin": "https://steamcommunity.com",
    "Referer": "https://steamcommunity.com/",
}


def apply_session_credentials(creds: dict[str, str] | None = None) -> dict[str, str]:
    """Reload cookies from state.json into the shared requests session."""
    if creds is None:
        creds = load_session_credentials()

    session.cookies.set(
        "sessionid",
        creds["sessionid"],
        domain="steamcommunity.com",
    )
    session.cookies.set(
        "steamLoginSecure",
        creds["steamLoginSecure"],
        domain="steamcommunity.com",
    )
    return creds


apply_session_credentials()
