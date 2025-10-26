# SPDX-License-Identifier: MPL-2.0
param(
    [Parameter(Mandatory=$true)][string]$Task,
    [string[]]$MakeArgs
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptDir "..")
$ArgsList = @('-C', $RepoRoot, $Task)
if ($MakeArgs) {
    $ArgsList += $MakeArgs
}
& make @ArgsList
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
