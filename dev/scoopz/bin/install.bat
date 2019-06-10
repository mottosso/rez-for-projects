@echo off
setlocal

:: Leverage Rez's Python to avoid Python as a dependency
pushd %~dp0..\python
call rez python -m "" scoopz %*

:: Regarding pushd
:: rez-python does not consider PYTHONPATH, as it is
:: passed the -E argument to python.exe. Thus, we
:: leverage the fact that it considers whatever is on
:: its current working directory as a valid package.

:: Regarding the -m ""
:: rez-python considers the first unknown argument as an
:: argument to FILE, which is incorrect. In effect, ""
:: is accepted by rez-python, and internally discarded
:: as it is empty, which makes it ignored

:: No popd?
:: The call to `setlocal` makes anything happening inside
:: of this script isolated to this script, so pushd won't
:: affect the calling shell, and neither would popd.
