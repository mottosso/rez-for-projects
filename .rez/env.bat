@echo off

:: Install packages here
set REZ_LOCAL_PACKAGES_PATH=%~dp0..\.packages

:: Look for packages here
set REZ_PACKAGES_PATH=%~dp0..\.packages

:: Expose re, alias for rez env
set PATH=%~dp0..\bin;%PATH%

set PROMPT=$$ 
