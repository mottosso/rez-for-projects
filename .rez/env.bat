@echo off

where /q python
IF ERRORLEVEL 1 (
	goto nopython
)

where /q rez
IF ERRORLEVEL 1 (
	goto norez
)

:: Install packages here
set REZ_LOCAL_PACKAGES_PATH=%~dp0..\.packages

:: Look for packages here
set REZ_PACKAGES_PATH=%~dp0..\.packages

:: Expose re, alias for rez env
set PATH=%~dp0..\bin;%PATH%

set PROMPT=$$ 

:norez
    echo ---------------------------------
    echo Rez was not found on your PATH :(
    echo ---------------------------------
    pause
    exit 1

:nopython
    echo ---------------------------------
    echo Python was not found on your PATH :(
    echo ---------------------------------
    pause
    exit 1