Push-Location
cd $PSScriptRoot

mkdir .\releases -Force

$options = @{
  Path = @(
    "./__init__.py", 
    "./icons", 
    "./README.md", 
    "./manifest.json"
  )
  DestinationPath = "./releases/anki_memorizer.ankiaddon"
}

$archiveDir = "./releases"

if(!(Test-Path $archiveDir)){
  mkdir $archiveDir
}

Compress-Archive @options -Force

Pop-Location