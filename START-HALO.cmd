@echo off
setlocal
cd /d "%~dp0"
set "HALO_APP=%~dp0index.html"
if not exist "%HALO_APP%" (
  echo The application file is missing.
  echo Right-click the ZIP, choose Extract All, then run START-HALO.cmd from the extracted folder.
  pause
  exit /b 1
)
rem Open an installed browser directly instead of relying on the .html file association.
if exist "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe" (
  start "" "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe" --new-window "%HALO_APP%"
  exit /b 0
)
if exist "%ProgramFiles%\Microsoft\Edge\Application\msedge.exe" (
  start "" "%ProgramFiles%\Microsoft\Edge\Application\msedge.exe" --new-window "%HALO_APP%"
  exit /b 0
)
if exist "%ProgramFiles%\Google\Chrome\Application\chrome.exe" (
  start "" "%ProgramFiles%\Google\Chrome\Application\chrome.exe" --new-window "%HALO_APP%"
  exit /b 0
)
if exist "%LocalAppData%\Google\Chrome\Application\chrome.exe" (
  start "" "%LocalAppData%\Google\Chrome\Application\chrome.exe" --new-window "%HALO_APP%"
  exit /b 0
)
start "" "%HALO_APP%"
