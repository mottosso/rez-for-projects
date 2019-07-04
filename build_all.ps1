$here = split-path -parent $PSCommandPath
$repo = split-path -parent $here

$env:REZ_CONFIG_FILE=join-path $repo "rezconfig.py"

& python $here\.rez\build_all.py $args
pause