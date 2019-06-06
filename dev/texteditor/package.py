name = "texteditor"
version = "2.0.1"
category = "ext"
requires = []

build_command = "python -m rezutils build {root}"
private_build_requires = ["rezutils-1"]

tools = [
    "texteditor",
]

_icons = {
    "32x32": "{root}/resources/icon_128.png",
    "64x64": "{root}/resources/icon_128.png",
}


def commands():
    global env

    env.PATH.append("{root}/bin")
