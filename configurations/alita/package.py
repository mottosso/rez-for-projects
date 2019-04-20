name = "alita"
version = "0.3.17"

requires = [
    "rezutils-1",
    "base-1",
    "python-2.7",

    # Supported DCCs, if either of these are used,
    # this must be their version.
    "~maya-2018",
    "~nuke-11",
    "~houdinifx-17",
    "~aftereffects-cs6",
    "~photoshop-2018",
]

environ = {
    "PROJECT_NAME": "Alita",
    "PROJECT_PATH": "{env.PROJECTS_PATH}/alita",

    # For locating in e.g. ftrack
    "PRODUCTION_TRACKER_ID": "alita-123",
}

maya_environ = {
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


def commands():
    global env
    global this
    global request
    global expandvars

    environ = this.environ

    if "maya" in request:
        environ.update(this.maya_environ)

    for key, value in this.environ.items():
        if isinstance(value, (tuple, list)):
            [env[key].append(expandvars(v)) for v in value]
        else:
            env[key] = expandvars(value)
