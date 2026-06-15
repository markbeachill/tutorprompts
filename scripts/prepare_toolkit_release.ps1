param(
    [Parameter(Mandatory=$true)][string]$Version,
    [string]$Date = ""
)

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent $scriptDir
Set-Location $repoRoot

if ($Date -eq "") {
    python scripts\prepare_toolkit_release.py --version $Version
} else {
    python scripts\prepare_toolkit_release.py --version $Version --date $Date
}
python scripts\build_prompt_libraries.py
python scripts\build_prompt_libraries.py --ci
python scripts\build_site_package.py --run-generator-check --version $Version
