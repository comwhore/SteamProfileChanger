import json
import random
import time
from pathlib import Path

from config import TIMEOUT_SECONDS


def wait():
    time.sleep(TIMEOUT_SECONDS)



def weighted_choice(items):
    pool = []

    for item in items:
        weight = item.get("weight", 1)
        pool.extend([item] * weight)

    return random.choice(pool)



def load_json(name):
    path = Path(name)

    if not path.exists():
        return []

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)