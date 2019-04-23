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
set REZ_LOCAL_PACKAGES_PATH=%~dp0packages

:: Look for packages here
set REZ_PACKAGES_PATH=%~dp0packages

:: Expose re, alias for rez env
set PATH=%~dp0..\bin;%PATH%

set PROMPT=$$ 

set GITLAB_API_KEY=abc123
set FTRACK_API_KEY=abc123

goto success

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

:success
