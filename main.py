from avatar import (
    get_local_avatar,
    upload_local_avatar,
    set_steam_avatar
)

from profile import (
    change_profile,
    clear_aliases
)

from cosmetics import (
    apply_avatar_frame,
    apply_background,
    apply_miniprofile,
    apply_theme,
    apply_badge,
    apply_all_cosmetics
)

from utils import (
    weighted_choice,
    load_json,
    wait
)

from nickname_gen.generator import Generator
from nickname_gen.wtypes import WordList, WordType, Lang

import random
import string

# Customize these lists for your own names and bios (see main.py.backup for a full example).
my_adjectives = WordList(
    "My Adjectives",
    Lang.EN,
    [
        "YOUR_ADJECTIVE_1",
        "YOUR_ADJECTIVE_2",
        "EMPTYREPLACE",
    ],
    WordType.ADJECTIVE
)

my_nouns = WordList(
    "My Nouns",
    Lang.EN,
    [
        "YOUR_NOUN_1",
        "YOUR_NOUN_2",
    ],
    WordType.NOUN
)

custom = [
    "YOUR_CUSTOM_NAME_1",
    "YOUR_CUSTOM_NAME_2",
]

beggining = [
    "YOUR_BEGINNING_1",
    "YOUR_BEGINNING_2",
]

middle = [
    "YOUR_MIDDLE_1",
    "YOUR_MIDDLE_2",
]

end = [
    "YOUR_ENDING_1",
    "YOUR_ENDING_2",
]

customBIOS = [
    "YOUR_CUSTOM_BIO_1",
    "YOUR_CUSTOM_BIO_2",
]


def main():
    from session_loader import ensure_session_valid
    from steam_client import apply_session_credentials

    apply_session_credentials(ensure_session_valid())

    rand = random.randint(1, 100)
    name: str = ""
    summary: str = ""
    length = random.randint(15, 30)
    result = "".join(random.choice(string.ascii_letters) for _ in range(length))
    customURL: str = result

    if rand >= 50:
        name = Generator.get_random_en_nickname(combos=[my_adjectives, my_nouns])
        name = name.lower()
        name = name.replace("emptyreplace", "")
    elif rand <= 30:
        name = random.choice(custom)
    else:
        name = f"{random.choice(beggining)} {random.choice(middle)}"

    rand = random.randint(1, 3)
    if rand == 1:
        name = name.upper()
    elif rand == 2:
        name = name.lower()
    else:
        name = "".join(
            c.upper() if random.randint(1, 3) == 1 else c.lower()
            for c in name
        )

    rand = random.randint(1, 100)
    if rand <= 40:
        summary = random.choice(customBIOS)
    elif rand <= 10:
        summary = ""
    else:
        summary = (
            f"{random.choice(beggining)} {random.choice(middle)} "
            f"| {random.choice(end)}"
        )

    change_profile(name, summary, customURL)
    clear_aliases()
    wait()
    local_avatar = get_local_avatar()

    rand = random.randint(1, 100)

    if rand <= 50 or not local_avatar:
        set_steam_avatar()
    elif local_avatar:
        upload_local_avatar(local_avatar)

    wait()
    apply_all_cosmetics()

    print("[+] Finished")


if __name__ == "__main__":
    main()
