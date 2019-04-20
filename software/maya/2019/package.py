name = "maya"
version = "2019.0.1"
requires = []
build_command = False


def commands():
    import os
    global env
    global system

    if system.platform == "windows":
        path = r"c:\program files\autodesk\maya2019\bin"

    elif system.platform == "linux":
        path = "/opt/maya2019/bin"

    assert os.path.exists(path), "Missing files: %s" % path
    env["PATH"].prepend(path)
