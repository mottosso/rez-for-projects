@echo off
setlocal

where /q rez
IF ERRORLEVEL 1 (
	goto end
)

call %~dp0.rez\env.bat
call type %~dp0.rez\banner.txt
call cmd /k
exit 0

:end
    echo ---------------------------------
    echo Rez was not found on your PATH :(
    echo ---------------------------------
    pause
    exit 1