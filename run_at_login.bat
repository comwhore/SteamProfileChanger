@echo off
REM Hidden launcher; paths are relative to this file's folder.
powershell.exe -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File "%~dp0run_at_login.ps1"
