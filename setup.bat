@echo off

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed on your system. Installing Python...

    exit /b 1
)

python -m pip show psutil pyperclip tk >nul 2>&1
if %errorlevel% neq 0 (
    echo psutil colorama module is not installed. Installing psutil colorama...
    python -m pip install psutil pyperclip tk
    if %errorlevel% equ 0 (
        echo Installation of psutil pyperclip tk completed successfully!
    ) else (
        echo An error occurred while installing the psutil colorama module.
    )
) else (
    echo psutil colorama module is already installed.
)

echo All necessary components are installed.
echo You can now proceed with your tasks.

pause
