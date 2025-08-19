@ECHO OFF
REM Recreate the devagents directory
IF EXIST devagents RMDIR /S /Q devagents
MKDIR devagents

REM Copy the necessary root level files
COPY ..\*.* devagents
DEL devagents\.env
DEL devagents\.gitignore
DEL devagents\_venv.bat
DEL devagents\_format_all.ps1

REM Copy the necessary subdirectories
XCOPY ..\utils\* devagents\utils /I /Y /S
XCOPY ..\tools\* devagents\tools /I /Y /S
XCOPY ..\scenarios\* devagents\scenarios /I /Y /S
XCOPY ..\agents\* devagents\agents /I /Y /S
XCOPY ..\monitoring\* devagents\monitoring /I /Y /S
XCOPY ..\scenario_engine\* devagents\scenario_engine /I /Y /S
XCOPY ..\cli\* devagents\cli /I /Y /S

REM Copy the tests
MKDIR devagents\tests
COPY ..\tests\*.* devagents\tests
XCOPY ..\tests\test_data\* devagents\tests\test_data /I /Y /S

REM Update the Build number
python update_build.py

REM Build the Docker image
docker build -t devagents .
