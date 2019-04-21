name = "pyblish_base"
version = "1.4.2"

private_build_requires = [
    "rezutils-1",
]

environ = {
    "PYTHONPATH": [
        "{root}/python",
    ],
}

build_command = "python -m rezutils {root}"


def commands():
    global env
    global this
    global system
    global expandvars

    for key, value in this.environ.items():
        if isinstance(value, (tuple, list)):
            [env[key].append(expandvars(v)) for v in value]
        else:
            env[key] = expandvars(value)
