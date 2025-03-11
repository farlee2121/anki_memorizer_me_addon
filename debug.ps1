Push-Location
cd $PSScriptRoot

Get-process -Name anki -ErrorAction SilentlyContinue | stop-process
.\pack.ps1

ii .\releases\anki_memorizer.ankiaddon

Pop-Location