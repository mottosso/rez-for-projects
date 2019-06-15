$here = split-path -parent $PSCommandPath
$rez = join-path $here ".rez"
. $rez\env.ps1
get-content -Path $rez\banner.txt
