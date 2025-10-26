# SPDX-License-Identifier: MPL-2.0
param(
    [string[]]$Args
)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Fix = $false
$Forward = @()
foreach ($arg in $Args) {
    if ($arg -eq '--fix') {
        $Fix = $true
    } else {
        $Forward += $arg
    }
}
$env:MSK_ARGS = [string]::Join(' ', $Forward)
if ($Fix) {
    $env:MSK_FIX = '1'
} else {
    Remove-Item Env:MSK_FIX -ErrorAction SilentlyContinue
}
& (Join-Path $ScriptDir 'run-task.ps1') -Task 'clean' -MakeArgs $null
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
