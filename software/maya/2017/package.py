name = "maya"
version = "2017.0.1"
requires = []
build_command = False


def commands():
    global env
    global system

    if system.platform == "windows":
        env["PATH"].prepend(r"c:\program files\autodesk\maya2017\bin")

    elif system.platform == "linux":
        env["PATH"].prepend("/opt/maya2017/bin")
