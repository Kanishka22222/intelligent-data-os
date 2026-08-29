@echo off
echo ===================================================
echo   Pushing DataOS to GitHub (Clean Initial Commit)
echo ===================================================
set "PATH=%~dp0..\mingit\cmd;%PATH%"
git push -u --force origin main
pause
