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
set REZ_LOCAL_PACKAGES_PATH=%~dp0..\local_packages_path
set REZ_RELEASE_PACKAGES_PATH=%~dp0..\release_packages_path

:: Look for packages here
set REZ_PACKAGES_PATH=%REZ_RELEASE_PACKAGES_PATH%;%REZ_LOCAL_PACKAGES_PATH%

:: "Aliases"
doskey re=rez env $*
doskey ri=rez build --install $*

set PROMPT=$$ 

set GITLAB_API_KEY=abc123
set FTRACK_API_KEY=abc123

goto success

:norez
    echo ---------------------------------
    echo Rez was not found on your PATH :(
    echo ---------------------------------
    pause

:nopython
    echo ---------------------------------
    echo Python was not found on your PATH :(
    echo ---------------------------------
    pause

:success
