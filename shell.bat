@echo off
setlocal

where /q rez
IF ERRORLEVEL 1 (
	goto end
)

:: Install packages here
set REZ_LOCAL_PACKAGES_PATH=%~dp0.packages

:: Look for packages here
set REZ_PACKAGES_PATH=%~dp0.packages

:: Expose rezutils.py to build step
rem set PYTHONPATH=%~dp0python
rem set REZ_PACKAGE_DEFINITION_BUILD_PYTHON_PATHS=%~dp0python
rem set REZ_PACKAGE_DEFINITION_PYTHON_PATH=%~dp0python

:: Expose re, alias for rez env
set PATH=%~dp0bin;%PATH%

set PROMPT=$$ 

call cat %~dp0banner.txt
call cmd /k
exit 0

:end
    echo ---------------------------------
    echo Rez was not found on your PATH :(
    echo ---------------------------------
    pause
    exit 1