@echo off

where /q python
IF ERRORLEVEL 1 (
	goto nopython
)

where /q rez
IF ERRORLEVEL 1 (
	goto norez
)

set REZ_CONFIG_FILE=%~dp0..\rezconfig.py

:: "Aliases"
doskey re=rez env $*
doskey ri=rez build --install $*

set PROMPT=(rez) $$ 

set GITLAB_API_KEY=abc123
set FTRACK_API_KEY=abc123

goto success

:norez
    echo ---------------------------------
    echo Rez was not found on your PATH :(
    echo ---------------------------------
    pause
    set ERRORLEVEL=1
    goto success

:nopython
    echo ---------------------------------
    echo Python was not found on your PATH :(
    echo ---------------------------------
    pause
    set ERRORLEVEL=1
    goto success

:success
