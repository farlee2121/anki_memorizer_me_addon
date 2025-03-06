Push-Location
cd $PSScriptRoot

mkdir .\releases -Force

$options = @{
  Path = @(
    "./__init__.py", 
    "./icons", 
    "./readme.md", 
    "./manifest.json"
  )
  DestinationPath = "./releases/anki_memorizer.ankiaddon"
}

Compress-Archive @options -Force

Pop-Location