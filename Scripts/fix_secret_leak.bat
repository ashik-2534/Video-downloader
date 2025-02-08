@echo off
:: Automatically detect and navigate to the script's directory
cd /d "%~dp0"

echo Installing GitGuardian CLI...
pip install ggshield || echo Failed to install ggshield. Install Python and pip first. & exit /b

echo Scanning repository for secrets...
ggshield scan repo . || echo Scan failed. Check manually. & exit /b

echo Downloading BFG Repo-Cleaner...
powershell Invoke-WebRequest -Uri "https://repo1.maven.org/maven2/com/madgag/bfg/1.14.0/bfg-1.14.0.jar" -OutFile "bfg.jar"

set /p SECRET="Enter the leaked secret to remove: "
echo %SECRET% > secrets.txt

echo Running BFG to remove the secret...
java -jar bfg.jar --replace-text secrets.txt || echo BFG failed. Try manual removal. & exit /b

echo Cleaning up Git history...
git reflog expire --expire=now --all
git gc --prune=now
git push origin --force --all

echo Rotate your secret in your service provider (API, AWS, etc.) and update your .env file.

echo Ensuring .env is ignored...
echo .env >> .gitignore
git add .gitignore
git commit -m "Added .env to .gitignore"
git push origin main

echo Installing GitGuardian pre-commit hooks...
ggshield install --mode pre-commit

echo ✅ Secret removed and protection enabled! Don't forget to rotate your secret.
pause
