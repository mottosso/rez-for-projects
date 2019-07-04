# An example of a package referencing something from outside
# of the local package.

name = "maya"
version = "2019.0.0"
requires = []

build_command = "python -m rezutil build {root}"
private_build_requires = ["rezutil-1"]

# Cross-platform binaries (i.e. shell scripts)
# are built and deployed with this package.
tools = [
    "maya",
    "mayapy",
    "render",
    "mayabatch",
    "mayagui_lic",
]

_category = "app"
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
