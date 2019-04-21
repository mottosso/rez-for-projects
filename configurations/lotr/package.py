name = "lotr"
version = "1.13.2"

requires = [
    "base-1",

    # DCCs
    "~maya-2011",
    "~nuke-9",
    "~houdinifx-11",
    "~mari-0.2",
]

build_command = "python -m rezutils {root}"

private_build_requires = [
    "rezutils-1",
]

environ = {
    "PROJECT_NAME": "Lord of the Rings",
    "PROJECT_PATH": "{env.PROJECTS_PATH}/lotr",

    # For locating in e.g. ftrack
    "PRODUCTION_TRACKER_ID": "lotr-124",
}


def commands():
    global env
    global this
    global expandvars

    for key, value in this.environ.items():
        if isinstance(value, (tuple, list)):
            [env[key].append(expandvars(v)) for v in value]
        else:
            env[key] = expandvars(value)
