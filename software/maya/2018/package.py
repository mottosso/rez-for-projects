# An example of a package referencing something from outside
# of the local package.

name = "maya"
version = "2018.0.1"
requires = []

build_command = "python -m rezutils {root}"

private_build_requires = [
    "rezutils-1",
]

# Cross-platform binaries (i.e. shell scripts)
# are built and deployed with this package.
tools = [
    "maya",
    "render",
    "mayabatch",
    "mayagui_lic",
]


def commands():
    import os
    global env
    global system

    if system.platform == "windows":
        path = r"c:\program files\autodesk\maya2018\bin"

    elif system.platform == "linux":
        path = "/opt/maya2018/bin"

    assert os.path.exists(path), "Missing files: %s" % path

    env["MAYA_BIN_DIR"] = path
    env["MAYA_BIN_ARGS"] = (

        # Manage plug-in loading manually
        "-noAutoloadPlugins" +

        # Python 3 compatibility warnings
        " -3"
    )

    env["PATH"].prepend("{root}/bin")
