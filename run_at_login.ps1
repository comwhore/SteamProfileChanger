# Runs main.py from this script's folder (move-safe). Used by the logon scheduled task.
$ProjectDir = $PSScriptRoot
Set-Location $ProjectDir

$logDir = Join-Path $ProjectDir "logs"
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir | Out-Null
}

$logFile = Join-Path $logDir ("login_{0:yyyyMMdd}.log" -f (Get-Date))

function Write-Log($message) {
    $line = "[{0}] {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $message
    Add-Content -Path $logFile -Value $line -Encoding UTF8
}

Write-Log "Starting main.py in $ProjectDir"

$exitCode = 0
try {
    if (Get-Command py -ErrorAction SilentlyContinue) {
        $output = & py -3 main.py 2>&1
    } else {
        $output = & python main.py 2>&1
    }

    $exitCode = $LASTEXITCODE

    if ($output) {
        Add-Content -Path $logFile -Value ($output | Out-String).TrimEnd() -Encoding UTF8
    }
} catch {
    Write-Log "Error: $_"
    $exitCode = 1
}

Write-Log "Exit code $exitCode"
