# An example of a package referencing something from outside
# of the local package.

name = "dev_maya"
version = "2018.1.0"
requires = []

build_command = "python -m rezutils build {root}"
private_build_requires = ["rezutils-1"]

# Cross-platform binaries (i.e. shell scripts)
# are built and deployed with this package.
tools = [
    "maya",
    "mayapy",
    "render",
    "mayabatch",
]

_category = "app"
_data = {
    "label": "Developer Maya",
    "color": "#512",
    "icons": {
        "32x32": "{root}/resources/icon_256x256.png",
        "64x64": "{root}/resources/icon_256x256.png",
    },
}


def commands():
    global env
    env.PATH.prepend("{root}/bin")
