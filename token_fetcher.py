import base64
import json
import re
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

STEAM_URL = "https://steamcommunity.com"
TOKEN_CACHE_PATH = Path(".token_cache.json")
STATE_PATH = Path("state.json")
# Refresh before Playwright if cache is older than this (seconds)
CACHE_MAX_AGE = 50 * 60


def _jwt_exp_unix(token: str) -> float | None:
    try:
        part = token.split(".")[1]
        part += "=" * (-len(part) % 4)
        payload = json.loads(base64.urlsafe_b64decode(part))
        exp = payload.get("exp")
        return float(exp) if exp is not None else None
    except (IndexError, ValueError, json.JSONDecodeError):
        return None


def _read_cache(steam_id: str) -> str | None:
    if not TOKEN_CACHE_PATH.is_file():
        return None
    try:
        data = json.loads(TOKEN_CACHE_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    if data.get("steam_id") != steam_id or not data.get("token"):
        return None
    expires_at = data.get("expires_at")
    if expires_at and time.time() < float(expires_at) - 120:
        return data["token"]
    return None


def _write_cache(steam_id: str, token: str) -> None:
    expires_at = _jwt_exp_unix(token) or (time.time() + CACHE_MAX_AGE)
    TOKEN_CACHE_PATH.write_text(
        json.dumps(
            {
                "steam_id": steam_id,
                "token": token,
                "expires_at": expires_at,
            }
        ),
        encoding="utf-8",
    )


def clear_token_cache() -> None:
    if TOKEN_CACHE_PATH.is_file():
        TOKEN_CACHE_PATH.unlink()


def fetch_access_token(steam_id: str, state_path: Path = STATE_PATH) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state=str(state_path))
        page = context.new_page()
        token = None

        def handle_response(response):
            nonlocal token
            match = re.search(r"access_token=([^&]+)", response.url)
            if match:
                token = match.group(1)

        page.on("response", handle_response)
        page.goto(f"{STEAM_URL}/profiles/{steam_id}/edit")
        page.wait_for_timeout(5000)

        # Persist any rotated cookies (sessionid, etc.) back to state.json
        context.storage_state(path=str(state_path))
        browser.close()

        if not token:
            clear_token_cache()
            raise RuntimeError(
                "Failed to get access token. Session may be expired — "
                "run: python setup_playwright.py"
            )

        return token


def get_access_token(steam_id: str, *, force_refresh: bool = False) -> str:
    if not force_refresh:
        cached = _read_cache(steam_id)
        if cached:
            return cached

    token = fetch_access_token(steam_id)
    _write_cache(steam_id, token)
    return token


if __name__ == "__main__":
    from session_loader import load_session_credentials

    creds = load_session_credentials()
    print(get_access_token(creds["steam_id"], force_refresh=True))
