Get-ChildItem *.py | ForEach-Object { isort $_.FullName }
Get-ChildItem *.py | ForEach-Object { black --line-length=120 $_.FullName }
Get-ChildItem -Recurse -Include *.py -Path agents, scenarios, tests, tools, utils | ForEach-Object { isort $_.FullName }
Get-ChildItem -Recurse -Include *.py -Path agents, scenarios, tests, tools, utils | ForEach-Object { black --line-length=120 $_.FullName }
