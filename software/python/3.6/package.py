# Rudimentary expose of system Python

name = "python"
version = "3.6"
requires = []

environ = {
    "PYTHONDONTWRITEBYTECODE": "1",
}

# Use system-python
build_command = False


def commands():
    import os
    global env
    global this
    global alias
    global system
    global expandvars

    if system.platform == "windows":
        exe = r"c:\python36\python.exe"
        env.PATH.append(os.path.dirname(exe))
    else:
        exe = "/usr/bin/python3.6"
        alias("python", exe)

    assert os.path.exists(exe), (
        "Python could not be found on this system"
    )

    environ = this.environ

    for key, value in environ.items():
        if isinstance(value, (tuple, list)):
            [env[key].append(expandvars(v)) for v in value]
        else:
            env[key] = expandvars(value)
