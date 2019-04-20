@echo off
setlocal

call %~dp0.rez\env.bat
call type %~dp0.rez\banner.txt
call cmd /k