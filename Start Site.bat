@echo off
title Constella - local server
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0Start-Site.ps1"
pause
