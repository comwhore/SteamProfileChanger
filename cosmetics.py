from steam_client import session, HEADERS
from utils import weighted_choice, load_json, wait
from config import STEAM_ID
from token_fetcher import get_access_token


API_BASE = "https://api.steampowered.com/IPlayerService"


def post_protobuf(endpoint, protobuf, access_token: str):
    url = f"{API_BASE}/{endpoint}?access_token={access_token}"

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

    print(f"[*] {endpoint}: {response.status_code}")
    print(response.text[:300])

    return response


def apply_all_cosmetics():
    cosmetics = [
        (
            "frames.json",
            "SetAvatarFrame/v1",
            "avatar frame"
        ),

        (
            "backgrounds.json",
            "SetProfileBackground/v1",
            "background"
        ),

        (
            "miniprofiles.json",
            "SetMiniProfileBackground/v1",
            "mini profile"
        ),

        (
            "themes.json",
            "SetProfileTheme/v1",
            "theme"
        ),

        (
            "badges.json",
            "SetFavoriteBadge/v1",
            "badge"
        )
    ]

    access_token = get_access_token(STEAM_ID)

    for json_file, endpoint, label in cosmetics:
        items = load_json(json_file)

        if not items:
            continue

        chosen = weighted_choice(items)

        protobuf = chosen.get("protobuf")

        if not protobuf:
            print(f"[!] Missing protobuf in {json_file}")
            continue

        print(f"[*] Applying {label}")

        post_protobuf(endpoint, protobuf, access_token)

        wait()


def apply_avatar_frame():
    apply_all_cosmetics()


def apply_background():
    apply_all_cosmetics()


def apply_miniprofile():
    apply_all_cosmetics()


def apply_theme():
    apply_all_cosmetics()


def apply_badge():
    apply_all_cosmetics()

