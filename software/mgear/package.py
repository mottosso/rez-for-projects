name = "mgear"
version = "2.4.1"

private_build_requires = [
    "rezutils-1",
]

requires = [
    "~maya>=2016,<2019",
]

environ = {
    "MGEAR_SHIFTER_CUSTOMSTEP_PATH": "{root}/python/mGear/build/custom_steps",
    "MGEAR_SHIFTER_COMPONENT_PATH": "{root}/python/mGear/build/components",
    "MGEAR_SYNOPTIC_PATH": "{root}/python/mGear/env/synoptic",
}


def commands():
    global env
    global this
    global expandvars

    environ = this.environ

    for key, value in environ.items():
        if isinstance(value, (tuple, list)):
            [env[key].append(expandvars(v)) for v in value]
        else:
            env[key] = expandvars(value)
