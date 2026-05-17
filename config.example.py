from token_fetcher import fetch_access_token

# Session ID and Steam Login Secure are found in the browser cookies
SESSION_ID = "YOUR_SESSION_ID_HERE"
STEAM_LOGIN_SECURE = "YOUR_STEAM_LOGIN_SECURE_HERE"
STEAM_ID = "YOUR_STEAM_ID_HERE"
TIMEOUT_SECONDS = 3
ACCESS_TOKEN = fetch_access_token()
