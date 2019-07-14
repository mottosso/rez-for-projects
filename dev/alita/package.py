name = "alita"
version = "0.3.20"

build_command = "python -m rezutil build {root}"
private_build_requires = ["rezutil-1"]

# Variables unrelated to Rez are prefixed with `_`
# These are managed by the recipient via the Rez API
_category = "proj"
_data = {
    "label": "Alita - Battle Angel",
    "icon": "{root}/resources/icon_{width}x{height}.png"
}

_requires = {
    "any": [
        "welcome-1",
        "base-1",

        # Supported DCCs, if either of these are used,
        # this must be their version.
        "~maya-2018",
        "~dev_maya2",  # hidden
        "~nuke-11",
        "~terminal",
    ],

    # Requirements relative a request
    # E.g. if `alita maya` is requested, the "maya"
    # requirements are added to the list.
    "maya": [
        "maya_base",
        "mgear-2.4",
    ],
    "nuke": [
    ]
}

_environ = {
    "any": {
        "PROJECT_NAME": "Alita",
        "PROJECT_PATH": "{env.PROJECTS_PATH}/alita",

        # For locating in e.g. ftrack
        "PRODUCTION_TRACKER_ID": "alita-123",
    },

    # Global overrides for TDs and free-form scripts
    # These lack version or write-access control, and
    # are intended for quick hacks and experimentation
    # by artists not familiar or involved with Rez
    # or overall package distribution.
    "maya": {
        "MAYA_COLOR_MANAGEMENT_POLICY_FILE": [
            "{env.PROJECT_PATH}/maya/color_management"
            "/default_synColorConfig.xml"
        ],

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

# ---------
#
# Internal
#
# ---------

late = locals()["late"]


@late()
def requires():
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
