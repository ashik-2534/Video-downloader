@echo off
setlocal

:: Ask for the repository name
set /p repo_name="Enter the repository name: "

:: Set your GitHub username (CHANGE THIS to your actual username)
set GITHUB_USERNAME=ashik-2534

:: Construct the remote URL
set REMOTE_URL=https://github.com/%GITHUB_USERNAME%/%repo_name%.git

:: Check if the remote URL already exists
git remote get-url origin >nul 2>nul
if %errorlevel% equ 0 (
    echo Remote URL already exists. Updating the remote URL...
    git remote set-url origin %REMOTE_URL%
) else (
    echo Adding new remote URL: %REMOTE_URL%
    git remote add origin %REMOTE_URL%
)

:: Verify the remote URL
echo Remote URL set to: %REMOTE_URL%

:: Rename branch to main (if not already main)
git branch -M main

:: Push the main branch to GitHub
git push -u origin main

endlocal
