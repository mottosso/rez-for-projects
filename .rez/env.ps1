$here = split-path -parent $PSCommandPath
$repo = split-path -parent $here

$env:REZ_RELEASE_PACKAGES_PATH=join-path $repo "packages"
$env:REZ_CONFIG_FILE=join-path $repo "rezconfig.py"

function prompt {"<rez> $ "}

function re { rez env $args }
function rb { rez build --install $args }

$env:GITLAB_API_KEY = "abc123"
$env:FTRACK_API_KEY = "abc123"
