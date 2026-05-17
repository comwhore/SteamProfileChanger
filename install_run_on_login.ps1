# Registers SteamProfileChanger to run main.py at Windows logon (hidden, no console).
#
# Install:   powershell -ExecutionPolicy Bypass -File install_run_on_login.ps1
# Uninstall: powershell -ExecutionPolicy Bypass -File install_run_on_login.ps1 -Uninstall
#
# After moving this project folder, run Install again from the new location.

param(
    [switch]$Uninstall
)

$TaskName = "SteamProfileChanger"
$ProjectDir = $PSScriptRoot
$RunnerPs1 = Join-Path $ProjectDir "run_at_login.ps1"

if ($Uninstall) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
    Write-Host "Removed logon task '$TaskName'."
    exit 0
}

if (-not (Test-Path $RunnerPs1)) {
    Write-Error "Missing run_at_login.ps1 in $ProjectDir"
    exit 1
}

$psArgs = "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$RunnerPs1`""

$action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument $psArgs `
    -WorkingDirectory $ProjectDir

$trigger = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME

$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Hours 1)

$existing = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($existing) {
    $oldArgs = $existing.Actions[0].Arguments
    if ($oldArgs -and $oldArgs -notmatch [regex]::Escape($ProjectDir)) {
        Write-Host "Updating task paths (folder may have moved)."
    }
}

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Description "Runs SteamProfileChanger main.py at user logon (hidden)." `
    -Force | Out-Null

Write-Host "Installed logon task '$TaskName' (hidden)."
Write-Host "  Project: $ProjectDir"
Write-Host "  Runner:  $RunnerPs1"
Write-Host "  Logs:    $ProjectDir\logs\"
Write-Host ""
Write-Host "If you move this folder later, run this installer again from the new path."
Write-Host ""
Write-Host "To remove: powershell -ExecutionPolicy Bypass -File install_run_on_login.ps1 -Uninstall"
