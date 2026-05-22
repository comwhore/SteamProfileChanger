# SteamProfileChanger

Unofficial Steam profile customization tool.

## Features

- Random name changer from list
- Alias history clearer
- Random avatar changer
- Profile cosmetics (frames, backgrounds, mini profiles, themes, badges) changer

Perfect for constantly anonymizing your profile.

---

## Installation

Install Python 3, then:

```bash
pip install -r requirements.txt
playwright install chromium
```

Copy the example config (never commit `config.py`):

```bash
copy config.example.py config.py
```

On Linux/macOS use `cp` instead of `copy`.

Session cookies and SteamID64 are read automatically from `state.json` (see Playwright session below). You do not paste `sessionid` or `steamLoginSecure` into `config.py` by hand.

---

## Configuration files

| Examples | Your local file should be |
|---------------------|------------------------------|
| `avatars.example.json` | `avatars.json` |
| `badges.example.json` | `badges.json` |
| `frames.example.json` | `frames.json` |
| `backgrounds.example.json` | `backgrounds.json` |
| `miniprofiles.example.json` | `miniprofiles.json` |


**Important:** The `.example.json` files use placeholder values (`ID_HERE`, `PROTOBUF_HERE`). They will **not** work until you replace them with real Steam item IDs and protobuf strings from your own account or captures. Also once you fill them, rename them to normal.

---

## Playwright session (`state.json`)

Log in once and save browser state (this supplies `sessionid`, `steamLoginSecure`, SteamID64, and the access token):

```bash
python setup_playwright.py
```

Log in in the opened browser, press Enter, then `state.json` is written locally. Keep it private.

Re-run this when you get signed out or when the script warns that login cookies are expiring.

**Access tokens:** Cosmetics/avatar API tokens are cached in `.token_cache.json` (~50 minutes). Playwright only runs when the cache is missing or expired, and then refreshes `state.json` cookies. Profile edits use `requests` only (no Playwright per run).

---

## Running

```bash
python main.py
```

---

## Avatar folder

Put image files in:

```text
pfps/
```

Supported: png, jpg, jpeg, webp, gif

This folder is gitignored.

---

## Run on Windows logon

See `install.md`.

---

## Timeout

Change `TIMEOUT_SECONDS` in `config.py`.

---

## Notes

Steam may change endpoints at any time.

The alias clear endpoint currently used is:

```text
/ajaxclearaliashistory/
```

which appears to be undocumented.

Use at your own risk.
