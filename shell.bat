@echo off
setlocal

call %~dp0.rez\env.bat
if not ERRORLEVEL 1 (
	call type %~dp0.rez\banner.txt
	call cmd /k
)