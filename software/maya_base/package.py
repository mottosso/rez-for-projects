name = "maya_base"
version = "1.0.7"
requires = [
    "core_pipeline-2",
]

build_command = False

environ = {
    "MAYA_DISABLE_CIP": "1",
    "MAYA_DISABLE_CER": "1",
    "MAYA_DISABLE_CLIC_IPM": "1",

    "MAYA_ENABLE_LEGACY_VIEWPORT": "1",
    "MAYA_VP2_DEVICE_OVERRIDE": "VirtualDeviceDx11",

    "MAYA_DISABLE_CLIC_IPM": "1",
    "MAYA_FORCE_PANEL_FOCUS": "0",
    "MAYA_DEBUG_SIGTERM_AS_SIGINT": "1",
    "MAYA_COLOR_MANAGEMENT_POLICY_LOCK": "1",
    "MAYA_RENDER_SETUP_INCLUDE_ALL_LIGHTS": "0",
}


def commands():
    global env
    global this
    global system
    global expandvars

    environ = this.environ

    for key, value in environ.items():
        if isinstance(value, (tuple, list)):
            [env[key].append(expandvars(v)) for v in value]
        else:
            env[key] = expandvars(value)
