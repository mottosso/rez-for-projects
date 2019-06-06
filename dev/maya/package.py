# An example of a package referencing something from outside
# of the local package.

name = "maya"
version = "2018.0.2"
category = "ext"
requires = []

build_command = "python -m rezutils build {root}"
private_build_requires = ["rezutils-1"]

# Cross-platform binaries (i.e. shell scripts)
# are built and deployed with this package.
tools = [
    "maya",
    "render",
    "mayabatch",
    "mayagui_lic",
]

_data = {
    "label": "Autodesk Maya",
    "color": "#251",
    "icons": {
        "32x32": "{root}/resources/icon_256x256.png",
        "64x64": "{root}/resources/icon_256x256.png",
    },
}


def commands():
    global env
    global alias
    global system

    env.PATH.prepend("{root}/bin")
