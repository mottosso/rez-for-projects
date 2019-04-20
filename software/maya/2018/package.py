name = "maya"
version = "2018.0.1"
requires = []
build_command = False


def commands():
    global env
    global system

    if system.platform == "windows":
        env["PATH"].prepend(r"c:\program files\autodesk\maya2018\bin")

    elif system.platform == "linux":
        env["PATH"].prepend("/opt/maya2018/bin")
