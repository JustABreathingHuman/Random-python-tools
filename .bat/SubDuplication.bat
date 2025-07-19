@echo off
setlocal enabledelayedexpansion
set "folderCount=3"
set "chars=ABCDEFGHIJKLMNOPQRSTUVWXYZ"
set "nameLength=16"
cd /d "%~dp0"
set /a totalCreated=0
echo Creating !folderCount! folders in each subdirectory...
:: Loop through all subdirectories
for /d /r %%D in (*) do (
    if exist "%%D" (
        for /l %%F in (1,1,!folderCount!) do (
            :: Generate a new random folder name
            set "randomName="
            for /l %%i in (1,1,!nameLength!) do (
                set /a rnd=!random! %% 26
                for %%c in (!rnd!) do (
                    set "randomName=!randomName!!chars:~%%c,1!"
                )
            )
            :: Create the folder
            md "%%D\!randomName!" 2>nul
            if exist "%%D\!randomName!" (
                set /a totalCreated+=1
            )
        )
    )
)

echo.
echo Created !totalCreated! folders total across all subdirectories.
pause
