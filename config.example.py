from session_loader import load_session_credentials

_credentials = load_session_credentials()

SESSION_ID = _credentials["sessionid"]
STEAM_LOGIN_SECURE = _credentials["steamLoginSecure"]
STEAM_ID = _credentials["steam_id"]
TIMEOUT_SECONDS = 3
