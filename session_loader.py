import json
import time
from pathlib import Path

STATE_PATH = Path("state.json")
STEAM_COMMUNITY = "steamcommunity.com"


def _jwt_exp_unix(token: str) -> float | None:
    import base64

    try:
        part = token.split(".")[1]
        part += "=" * (-len(part) % 4)
        payload = json.loads(base64.urlsafe_b64decode(part))
        exp = payload.get("exp")
        return float(exp) if exp is not None else None
    except (IndexError, ValueError, json.JSONDecodeError):
        return None


def _jwt_from_login_secure(steam_login_secure: str) -> str:
    if "%7C%7C" in steam_login_secure:
        return steam_login_secure.split("%7C%7C", 1)[1]
    if "||" in steam_login_secure:
        return steam_login_secure.split("||", 1)[1]
    return steam_login_secure


def load_session_credentials(state_path: Path = STATE_PATH) -> dict[str, str]:
    if not state_path.is_file():
        raise FileNotFoundError(
            f"{state_path} not found. Run: python setup_playwright.py"
        )

    with open(state_path, encoding="utf-8") as f:
        storage = json.load(f)

    cookies: dict[str, str] = {}
    for cookie in storage.get("cookies", []):
        domain = cookie.get("domain", "").lstrip(".")
        if domain != STEAM_COMMUNITY:
            continue
        cookies[cookie["name"]] = cookie["value"]

    session_id = cookies.get("sessionid")
    steam_login_secure = cookies.get("steamLoginSecure")

    if not session_id:
        raise ValueError(
            f"sessionid not found for {STEAM_COMMUNITY} in {state_path}"
        )
    if not steam_login_secure:
        raise ValueError(
            f"steamLoginSecure not found for {STEAM_COMMUNITY} in {state_path}"
        )

    steam_id = steam_login_secure.split("%7C%7C", 1)[0]
    if not steam_id.isdigit():
        raise ValueError("Could not parse SteamID64 from steamLoginSecure cookie")

    return {
        "sessionid": session_id,
        "steamLoginSecure": steam_login_secure,
        "steam_id": steam_id,
    }


def login_secure_expires_in(state_path: Path = STATE_PATH) -> float | None:
    """Seconds until steamLoginSecure JWT expires, or None if unknown."""
    creds = load_session_credentials(state_path)
    exp = _jwt_exp_unix(_jwt_from_login_secure(creds["steamLoginSecure"]))
    if exp is None:
        return None
    return exp - time.time()


def ensure_session_valid(state_path: Path = STATE_PATH) -> dict[str, str]:
    creds = load_session_credentials(state_path)
    remaining = login_secure_expires_in(state_path)
    if remaining is not None and remaining <= 0:
        raise RuntimeError(
            "steamLoginSecure has expired. Run: python setup_playwright.py"
        )
    if remaining is not None and remaining < 3600:
        print(
            f"[!] Steam login cookie expires in {int(remaining // 60)} min — "
            "re-run setup_playwright.py soon"
        )
    return creds
