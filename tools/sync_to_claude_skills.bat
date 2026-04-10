@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
set "PYTHON_SCRIPT=%SCRIPT_DIR%sync_to_claude_skills.py"

python "%PYTHON_SCRIPT%" --prune %*

if errorlevel 1 (
  echo.
  echo Sync failed.
  exit /b %errorlevel%
)

echo.
echo Sync finished successfully.
