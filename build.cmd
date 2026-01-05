cls
cd C:\Users\celio.jesus\OneDrive\WebServer\PromAPI
taskkill /FI "IMAGENAME eq Promapi.exe" /f

:: Delete previous builds
rmdir /s /q dist
rmdir /s /q build
del /q PromAPI.spec

:: Build new executable
pyinstaller --name PromAPI --onefile --add-data "util;util" --add-data "templates;templates" --add-data "static;static" --add-data "modules;modules" main_installer.py

