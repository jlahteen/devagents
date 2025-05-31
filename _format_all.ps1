# Root directory
Get-ChildItem *.py | ForEach-Object { isort $_.FullName }
Get-ChildItem *.py | ForEach-Object { black --line-length=120 $_.FullName }

# Subdirectories excluding tests
Get-ChildItem -Recurse -Include *.py -Path agents, scenarios, tools, utils | ForEach-Object { isort $_.FullName }
Get-ChildItem -Recurse -Include *.py -Path agents, scenarios, tools, utils | ForEach-Object { black --line-length=120 $_.FullName }

# tests directory
Get-ChildItem tests\*.py | ForEach-Object { isort $_.FullName }
Get-ChildItem tests\*.py | ForEach-Object { black --line-length=120 $_.FullName }
