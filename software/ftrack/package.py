# An example of how a third-party production tracker can
# be linked into a project.

name = "ftrack"
version = "1.0.0"
build_command = False

environ = {
    "FTRACK_URI": "ftrack.mystudio.co.jp",
    "FTRACK_PROTOCOL": "https",
}


def commands():
    import os
    global env
    global this
    global building

    # Ensure it isn't checked during a build, which would
    # prevent packages that require this package from being
    # built without having the key avaiable.
    if not building and "FTRACK_API_KEY" not in os.environ:
        print("WARNING: FTRACK_API_KEY missing")

    for key, value in this.environ.items():
        env[key] = value
