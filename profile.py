import re

from steam_client import session, HEADERS
from config import STEAM_ID
from session_loader import load_session_credentials


def _resolve_edit_urls() -> tuple[str, str]:
    r = session.get(
        f"https://steamcommunity.com/profiles/{STEAM_ID}/edit/info",
        headers=HEADERS,
        allow_redirects=True,
    )
    info_url = r.url
    if info_url.endswith("/edit/info"):
        edit_url = info_url[: -len("/edit/info")] + "/edit/"
    elif "/edit/info" in info_url:
        edit_url = info_url.replace("/edit/info", "/edit/")
    else:
        edit_url = info_url if info_url.endswith("/") else info_url + "/"
    return edit_url, info_url


def _profile_save_fields(
    session_id: str, name: str, summary: str, custom_url: str
) -> list[tuple[str, tuple[None, str]]]:
    plain = [
        ("sessionID", session_id),
        ("type", "profileSave"),
        ("weblink_1_title", ""),
        ("weblink_1_url", ""),
        ("weblink_2_title", ""),
        ("weblink_2_url", ""),
        ("weblink_3_title", ""),
        ("weblink_3_url", ""),
        ("personaName", name),
        ("real_name", ""),
        ("customURL", custom_url),
        ("country", ""),
        ("state", ""),
        ("city", ""),
        ("summary", summary),
        ("hide_profile_awards", "1"),
        ("type", "profileSave"),
        ("sessionID", session_id),
        ("json", "1"),
    ]
    return [(key, (None, value)) for key, value in plain]


def change_profile(name: str, summary: str, customURL: str):
    print(f"[*] Changing name to: {name}, summary to: {summary}, customURL to: {customURL}")

    session_id = load_session_credentials()["sessionid"]
    edit_url, referer = _resolve_edit_urls()
    fields = _profile_save_fields(session_id, name, summary, customURL)

    headers = {
        **HEADERS,
        "Accept": "application/json, text/plain, */*",
        "Referer": referer,
    }

    response = session.post(
        edit_url,
        headers=headers,
        files=fields,
    )

    print(response.status_code)
    try:
        result = response.json()
        print(result)
        if result.get("success") != 1:
            print(f"[!] Profile save failed: {result.get('errmsg', result)}")
    except ValueError:
        print(response.text[:500])


def clear_aliases():
    print("[*] Clearing aliases")

    url = (
        f"https://steamcommunity.com/profiles/"
        f"{STEAM_ID}/ajaxclearaliashistory/"
    )

    response = session.post(
        url,
        headers=HEADERS,
        data={
            "sessionid": load_session_credentials()["sessionid"]
        }
    )

    print(response.text)