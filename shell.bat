@echo off
setlocal

set REZ_DEFAULT_SHELL=powershell
powershell -noexit ". %~dp0shell.ps1"
