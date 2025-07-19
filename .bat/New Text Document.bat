@echo off
setlocal

:: Check if a file was dropped
if "%~1"=="" (
    echo Please drag and drop an executable onto this batch file.
    pause
    exit /b
)

:: Set the dropped file path
set "EXE_PATH=%~1"

:: Set __COMPAT_LAYER to RunAsInvoker to avoid UAC prompt
set __COMPAT_LAYER=RunAsInvoker

:: Run the dropped executable without elevation
start "" "%EXE_PATH%"
