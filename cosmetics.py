from steam_client import session, HEADERS
from utils import weighted_choice, load_json, wait
from config import ACCESS_TOKEN


API_BASE = "https://api.steampowered.com/IPlayerService"


def post_protobuf(endpoint, protobuf):
    url = (
        f"{API_BASE}/{endpoint}"
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

        post_protobuf(
            endpoint,
            protobuf
        )

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

