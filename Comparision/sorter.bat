@echo off
setlocal enabledelayedexpansion

:: Create "Scene" and "Mask" folders if they don't exist
if not exist "Scene" mkdir "Scene"
if not exist "Mask" mkdir "Mask"

:: Loop through all files in the current directory
for %%i in (*.png) do (
    set "filename=%%~ni"
    set "extension=%%~xi"
    
    :: Check if the filename ends with "_0"
    if "!filename:~-2!"=="_0" (
        move "%%i" "Scene\%%~nxi"
    ) 
    
    :: Check if the filename ends with "_1"
    if "!filename:~-2!"=="_1" (
        move "%%i" "Mask\%%~nxi"
    )
)

echo Files have been sorted.
pause
