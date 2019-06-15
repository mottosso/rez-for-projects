$here = split-path -parent $PSCommandPath
. $here\.rez\env.ps1
& python $here\.rez\build_all.py $args
pause