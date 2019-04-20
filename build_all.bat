@echo off

call %~dp0.rez\env.bat
python %~dp0.rez\build_all.py %*
