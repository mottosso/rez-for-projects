@echo off
setlocal

:: Leverage Rez's Python to avoid Python as a dependency
set CWD=%cd%
pushd %~dp0..\python
call rez python -u "" -m scoopz %cwd% %*

:: Regarding pushd
:: rez-python does not consider PYTHONPATH, as it is
:: passed the -E argument to python.exe. Thus, we
:: leverage the fact that it considers whatever is on
:: its current working directory as a valid package.

:: Regarding the -u ""
:: rez-python considers the second unknown argument as an
:: argument to FILE, which is incorrect. In effect, ""
:: is accepted by rez-python, and internally discarded
:: as it is empty, which makes it ignored

:: No popd?
:: The call to `setlocal` makes anything happening inside
:: of this script isolated to this script, so pushd won't
:: affect the calling shell, and neither would popd.

:: %cwd%?
:: Because we misuse Rez's Python by changing the current
:: working directory, it prevents the called Python from
:: knowing where it came from, breaking e.g. "--prefix ."
