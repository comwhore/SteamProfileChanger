from playwright.sync_api import sync_playwright
import re
import json


STEAM_URL = "https://steamcommunity.com"


def fetch_access_token():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True
        )

        context = browser.new_context(
            storage_state="state.json"
        )

        page = context.new_page()

        token = None

        def handle_response(response):
            nonlocal token

            url = response.url

            match = re.search(
                r"access_token=([^&]+)",
                url
            )

            if match:
                token = match.group(1)

        page.on("response", handle_response)

        page.goto(
            f"{STEAM_URL}/profiles/YOUR_STEAM_ID/edit"
        )

        page.wait_for_timeout(5000)

        browser.close()

        if not token:
            raise Exception(
                "Failed to get access token"
            )

        return token


if __name__ == "__main__":
    token = fetch_access_token()

    print(token)
