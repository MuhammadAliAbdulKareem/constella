@echo off
title Constella - local server
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\Start-Site.ps1"
pause
