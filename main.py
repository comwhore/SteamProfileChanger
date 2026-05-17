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
from datetime import datetime
today = datetime.today()

my_adjectives = WordList(
    "My Adjectives",
    Lang.EN,
    [
        "YOUR_ADJECTIVES_HERE",
        "EMPTYREPLACE - I recommend having a bunch of them, cuz why not? In the code they get replaced with nothing.",
    ],
    WordType.ADJECTIVE
)

my_nouns = WordList(
    "My Nouns",
    Lang.EN,
    [
        "YOUR_NOUNS_HERE",
    ],
    WordType.NOUN
)

custom = [
"YOUR_CUSTOM_NAMES_HERE",
]

beggining = [
"YOUR_BEGGININGS_HERE",
]
middle = [
"YOUR_MIDDLES_HERE",
]
end = [
"YOUR_ENDINGS_HERE",
]

customBIOS = [
"YOUR_CUSTOM_BIOS_HERE",
]
def main():
    rand = random.randint(1,100)
    name: str = ""
    summary: str = ""
    length = random.randint(15,30)  # Specify the length of the random string
    result = ''.join(random.choice(string.ascii_letters) for _ in range(length))
    customURL: str = result
    
    # name
    if rand >= 50:
        # You can use this if you want to use the nickname generator's custom combos that you added
        # name = Generator.get_random_en_nickname(combos=[my_adjectives, my_nouns])
        name = Generator.get_random_en_nickname() # This will use the default combos that are already in the generator
        name = name.lower()
        name = name.replace("emptyreplace", "")
    elif rand <= 30:
        rand = random.randint(0, len(custom)-1)
        name = custom[rand]
    else: # This will use names from the custom bios that you added, if you don't want to, get rid of it and change the elif above to just "else:"
        while True:
            name = (
                f"{random.choice(beggining)} "
                f"{random.choice(middle)}"
            )
            if len(summary) <= 32:
                break
    rand = random.randint(1,3)
    if rand == 1:
        name = name.upper()
    elif rand == 2:
        name = name.lower()
    else:
        nameArray = []
        i = 0
        while i < len(name):
            rand = random.randint(1,3)
            if rand == 1:
                nameArray.append(name[i].upper())
            else:
                nameArray.append(name[i].lower())
            i += 1
        name = "".join(nameArray)

    # bio
    rand = random.randint(1, 100)
    if rand <= 40:
        temp = customBIOS[random.randint(0,len(customBIOS)-1)]
        while name in temp:
            temp = customBIOS[random.randint(0,len(customBIOS)-1)]
        summary = temp
    elif rand <= 10:
        summary = ""
    else:
        summary = f"{beggining[random.randint(0,len(beggining)-1)]} {middle[random.randint(0, len(middle)-1)]} | {end[random.randint(0, len(end)-1)]}"
    
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