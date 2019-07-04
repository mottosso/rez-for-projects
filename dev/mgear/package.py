name = "mgear"
version = "2.4.1"

private_build_requires = [
    "rezutil-1",
]

build_command = "python -m rezutil {root}"

requires = [
    "~maya>=2016,<2019",
]

_category = "ext"
_environ = {
    "MGEAR_SHIFTER_CUSTOMSTEP_PATH": "{root}/python/mGear/build/custom_steps",
    "MGEAR_SHIFTER_COMPONENT_PATH": "{root}/python/mGear/build/components",
    "MGEAR_SYNOPTIC_PATH": "{root}/python/mGear/env/synoptic",
}


def commands():
    global env
    global this
    global expandvars

    _environ = this._environ

    for key, value in _environ.items():
        if isinstance(value, (tuple, list)):
            [env[key].append(expandvars(v)) for v in value]
        else:
            env[key] = expandvars(value)
