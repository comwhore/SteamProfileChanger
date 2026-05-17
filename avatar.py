import random
from pathlib import Path

from steam_client import session, HEADERS
from config import SESSION_ID, STEAM_ID, ACCESS_TOKEN
from utils import weighted_choice, load_json


LOCAL_EXTS = [
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp"
]


def get_local_avatar():
    p = Path("pfps")

    if not p.exists():
        return None

    files = [
        x for x in p.iterdir()
        if x.suffix.lower() in LOCAL_EXTS
    ]

    if not files:
        return None

    return random.choice(files)


def upload_local_avatar(path: Path):
    print(f"[*] Uploading local avatar: {path.name}")

    url = "https://steamcommunity.com/actions/FileUploader/"

    with open(path, "rb") as f:
        files = {
            "avatar": (
                "blob",
                f,
                "image/png"
            )
        }

        data = {
            "type": "player_avatar_image",
            "sId": STEAM_ID,
            "sessionid": SESSION_ID,
            "doSub": "1",
            "json": "1"
        }

        response = session.post(
            url,
            headers=HEADERS,
            data=data,
            files=files
        )

    print(response.text[:300])


def set_steam_avatar():
    avatars_data = load_json("avatars.json")
    avatars = avatars_data.get("avatars", [])

    if not avatars:
        print("[!] No avatars")
        return

    chosen = weighted_choice(avatars)

    protobuf = chosen.get("protobuf")

    if not protobuf:
        print("[!] Missing protobuf in avatars.json")
        return

    print(f"[*] Setting Steam avatar: {chosen['id']}")

    url = (
        "https://api.steampowered.com/"
        "IPlayerService/SetAnimatedAvatar/v1"
        f"?access_token={ACCESS_TOKEN}"
    )

    response = session.post(
        url,
        headers=HEADERS,
        files={
            "input_protobuf_encoded": (
                None,
                protobuf
            )
        }
    )

    print(response.status_code)
    print(response.text[:300])