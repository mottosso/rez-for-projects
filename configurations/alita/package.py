late = locals()["late"]

name = "alita"
version = "0.3.17"

build_command = "python -m rezutils {root}"
private_build_requires = ["rezutils-1"]

_requires = {
    "": [
        "base-1",
        "python-2.7",

        # Supported DCCs, if either of these are used,
        # this must be their version.
        "~maya-2018",
        "~nuke-11",
        "~houdinifx-17",
        "~aftereffects-cs6",
        "~photoshop-2018",
    ],

    # Requirements relative a request
    # E.g. if `alita maya` is requested, the "maya"
    # requirements are added to the list.
    "maya": [
        "pyblish_base-1.4",
        "mgear-2.4",
    ],
    "nuke": [
        "pyblish_base-1.4",
    ]
}

_environ = {
    "": {
        "PROJECT_NAME": "Alita",
        "PROJECT_PATH": "{env.PROJECTS_PATH}/alita",

        # For locating in e.g. ftrack
        "PRODUCTION_TRACKER_ID": "alita-123",
    },

    # Environment relative a request
    "maya": {
        "MAYA_COLOR_MANAGEMENT_POLICY_FILE": [
            "{root}/maya/color_management/default_synColorConfig.xml"
        ],

        "PYTHONPATH": [
            "{root}/maya/scripts",
            "{root}/maya/shelves",
        ],

        "MAYA_PLUG_IN_PATH": [
            "{root}/maya/plugins"
        ],

        "MAYA_SCRIPT_PATH": [
            "{root}/maya/scripts",
        ],

        "MAYA_SHELF_PATH": "{root}/maya/shelves",
        "XBMLANGPATH": [
            "{root}/maya/shelves/icons"
        ],
    }
}


@late()
def requires():
    global this
    global request
    global in_context

    _requires = this._requires
    requires = _requires[""][:]

    # Add DCC-specific requirements
    if in_context():
        for dcc in request:
            requires += _requires.get(dcc, [])

    return requires


def commands():
    global env
    global this
    global request
    global expandvars

    _environ = this._environ

    for name in request:
        _environ.update(_environ.get(name, {}))

    for key, value in _environ.items():
        if isinstance(value, (tuple, list)):
            [env[key].append(expandvars(v)) for v in value]
        else:
            env[key] = expandvars(value)
