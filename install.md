There are two parts: the app itself, and the **run on login** task.

## 1. App setup (one time)

1. Install **Python 3**.
2. In the project folder:
   ```bash
   pip install -r requirements.txt
   ```
3. Run `python setup_playwright.py` and save `state.json` (see `README.md`), then `copy config.example.py config.py`.
4. Test manually:
   ```bash
   python main.py
   ```
   or `py -3 main.py`

## 2. Install “run on login” (hidden)

1. Open **PowerShell** (or Terminal).
2. Go to the project folder, e.g.:
   ```powershell
   cd "C:\path\to\SteamProfileChanger"
   ```
3. Run the installer:
   ```powershell
   powershell -ExecutionPolicy Bypass -File .\install_run_on_login.ps1
   ```

You should see something like “Installed logon task `SteamProfileChanger` (hidden).”

After that, `main.py` runs automatically each time you sign in to Windows. Output goes to `logs\login_YYYYMMDD.log`.

## After you move the folder

Run step 2 again from the **new** path so Task Scheduler points at the right location.

## Remove it

From the project folder:

```powershell
powershell -ExecutionPolicy Bypass -File .\install_run_on_login.ps1 -Uninstall
```

## Optional check

- **Task Scheduler** → Task Scheduler Library → task named **`SteamProfileChanger`**
- Or sign out/in once and look for a new line in `logs\`

