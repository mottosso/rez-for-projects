name = "nuke"
version = "11.3.2"
requires = []
build_command = False


def commands():
    global env
    global system

    if system.platform == "windows":
        env["PATH"].prepend(r"c:\program files\nuke11.3v2\bin")

    elif system.platform == "linux":
        env["PATH"].prepend("/opt/nuke11.3v2/bin")
