# setup_browser.py

from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False
    )

    context = browser.new_context()

    page = context.new_page()

    page.goto(
        "https://steamcommunity.com/login/home/"
    )

    input(
        "Login fully then press ENTER..."
    )

    context.storage_state(
        path="state.json"
    )

    browser.close()
