# Root directory
Get-ChildItem *.py | ForEach-Object { isort $_.FullName }
Get-ChildItem *.py | ForEach-Object { black --line-length=120 $_.FullName }

# Subdirectories excluding tests
Get-ChildItem -Recurse -Include *.py -Path agents, agent_platform, scenarios, tools, utils, monitoring, scenario_engine, cli | ForEach-Object { isort $_.FullName }
Get-ChildItem -Recurse -Include *.py -Path agents, agent_platform, scenarios, tools, utils, monitoring, scenario_engine, cli | ForEach-Object { black --line-length=120 $_.FullName }

# tests directory
Get-ChildItem tests\*.py | ForEach-Object { isort $_.FullName }
Get-ChildItem tests\*.py | ForEach-Object { black --line-length=120 $_.FullName }
