name = "core_pipeline"
version = "2.1.0"

build_command = "python -m rezutil {root}"
private_build_requires = ["rezutil-1"]

_category = "int"
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
            [env[key].append(expandvars(v)) for v in value]
        else:
            env[key] = expandvars(value)
