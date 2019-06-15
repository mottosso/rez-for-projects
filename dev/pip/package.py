name = "pip"
version = "19.0.3"
requires = [
    "python>=2.7,<4",
]

build_command = "python -m rezutils {root}"
private_build_requires = ["rezutils-1"]

_category = "ext"
_environ = {
    "PYTHONPATH": [
        "{root}/python",
    ],
}


def commands():
    global env
    global this
    global system
    global expandvars

    for key, value in this._environ.items():
        if isinstance(value, (tuple, list)):
            [env[key].prepend(expandvars(v)) for v in value]
        else:
            env[key] = expandvars(value)
