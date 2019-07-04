name = "%(name)s"
version = "%(version)s"

## Subdirectory within which to release this package
category = "proj"

_requires = {
    "any": [
        "facility-1",

        ## Supported DCCs
        ## The "~" character denotes a "weak" requirement,
        ## meaning they aren't required by this project alone,
        ## but if explicitly requested then this must be their
        ## version.
        "~maya-2018",
        "~nuke-11",
    ],

    ## Requirements relative a request
    ## E.g. if `ATC maya` is requested, the "maya"
    ## requirements are added to the list.
    "maya": [
        "maya_base",
    ],
    "nuke": [],
    "houdini": [],
}

_environ = {
    "any": {
        "PROJECT_NAME": "%(name)s",
        "PROJECT_PATH": "{env.PROJECTS_PATH}/%(name)s",
    },

    ## Global overrides for TDs and free-form scripts
    ## Normally, these files are included alongside a
    ## package, e.g. "{root}/python". These are different.
    ## These lack version or write-access control, and
    ## are intended for quick hacks and experimentation
    ## by artists not familiar or involved with Rez
    ## or overall package distribution.
    "maya": {
        "PYTHONPATH": [
            "{env.PROJECT_PATH}/maya/scripts",
            "{env.PROJECT_PATH}/maya/shelves",
        ],

        "MAYA_PLUG_IN_PATH": [
            "{env.PROJECT_PATH}/maya/plugins"
        ],

        "MAYA_SCRIPT_PATH": [
            "{env.PROJECT_PATH}/maya/scripts",
        ],

        "MAYA_SHELF_PATH": "{env.PROJECT_PATH}/maya/shelves",
        "XBMLANGPATH": [
            "{env.PROJECT_PATH}/maya/shelves/icons"
        ],
    }
}

## ----------------------
##
## INTERNAL
##
## ----------------------

## The command used to bundle payload with package.py
build_command = "python -m rezutil build {root}"
private_build_requires = ["rezutil-1"]

## Below are boilerplate functionality to enable the above, do not touch
late = locals()["late"]


@late()
def requires():
    """Requirements relative a request

    This function merges a the "any" requirements with e.g. "maya"
    if "maya" is part of a request. Normally, every requirement
    is included with every request, but in this case we wouldn't want
    "maya" requirements included for e.g. "nuke" or "houdini" etc.
    The @late decorate makes this function get called at the time
    of calling `rez env` whereby `request` contains the requests
    made during that time.

    """

    global this
    global request
    global in_context

    requires = this._requires
    result = requires["any"][:]

    # Add request-specific requirements
    if in_context():
        for name, reqs in requires.items():
            if name not in request:
                continue

            result += reqs

    return result


def commands():
    global env
    global this
    global request
    global expandvars

    environ = this._environ
    result = list(environ["any"].items())

    # Add request-specific environments
    for key, values in environ.items():
        if key not in request:
            continue

        result += list(values.items())

    for key, value in result:
        if isinstance(value, (tuple, list)):
            [env[key].append(expandvars(v)) for v in value]
        else:
            env[key] = expandvars(value)
