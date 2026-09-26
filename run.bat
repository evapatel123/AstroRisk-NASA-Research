@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    echo AstroRisk environment not found.
    echo Run START_HERE.md first.
    pause
    exit /b 1
)
".venv\Scripts\python.exe" run.py
pause
