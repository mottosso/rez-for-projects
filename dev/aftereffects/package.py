# An example of a package referencing something from outside
# of the local package.

name = "aftereffects"
version = "cs6"
category = "ext"
requires = []

build_command = "python -m rezutils build {root}"
private_build_requires = ["rezutils-1"]

# Cross-platform binaries (i.e. shell scripts)
# are built and deployed with this package.
tools = [
    "nuke",
]

_icons = {
    "32x32": "{root}/resources/icon_256x256.png",
    "64x64": "{root}/resources/icon_256x256.png",
}


def commands():
    import os
    global env
    global alias
    global system

    if system.platform == "windows":
        bindir = "c:\\windows\\system32"

    elif system.platform == "linux":
        bindir = "/opt/nuke11.3v3/bin/"

    if not os.path.exists(bindir):
        print("WARNING: Missing files: %s" % bindir)

    bindir = "\"%s\"" % bindir

    # Add specific names to executables made
    # available by this package.
    alias("nuke", "notepad")
