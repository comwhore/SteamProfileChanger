from steam_client import session, HEADERS
from config import SESSION_ID, STEAM_ID



def change_profile(name: str, summary: str, customURL: str):
    print(f"[*] Changing name to: {name}, summary to: {summary}, customURL to: {customURL}")

    url = f"https://steamcommunity.com/profiles/{STEAM_ID}/edit/"

    data = {
        "sessionID": SESSION_ID,
        "type": "profileSave",
        "personaName": name,
        "real_name": "",
        "summary": summary,
        "country": "",
        "state": "",
        "city": "",
        "customURL": customURL,
        "hide_profile_awards": "1",
        "weblink_1_title": "",
        "weblink_1_url": "",
        "weblink_2_title": "",
        "weblink_2_url": "",
        "weblink_3_title": "",
        "weblink_3_url": "",
        "json": "1"
    }

    response = session.post(
        url,
        headers=HEADERS,
        data=data
    )

    print(response.status_code)

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
            "sessionid": SESSION_ID
        }
    )

    print(response.text)