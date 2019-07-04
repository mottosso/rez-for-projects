name = "texteditor"
version = "2.0.1"
requires = []

build_command = "python -m rezutil build {root}"
private_build_requires = ["rezutil-1"]

tools = [
    "texteditor",
]

_category = "app"
_data = {
    "icons": {
        "32x32": "{root}/resources/icon_128.png",
        "64x64": "{root}/resources/icon_128.png",
    }
}


def commands():
    global env

    env.PATH.append("{root}/bin")
