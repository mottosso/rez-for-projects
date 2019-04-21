# Required by every project

name = "base"
version = "1.2.1"
requires = [
    "ftrack-1",
    "gitlab-1",
]

environ = {
    "GITLAB_URI": "https://gitlab.mycompany.co.jp",
    "PROJECTS_PATH": "{this.projects_path}"
}

build_command = False


def commands():
    global env
    global this
    global system
    global expandvars

    # Base handles all differences between OSes
    # No reference to `system.platform` is made elsewhere
    if system.platform == "windows":
        this.projects_path = r"\\server\nas\projects"
    else:
        this.projects_path = "/mnt/projects"

    for key, value in this.environ.items():
        if isinstance(value, (tuple, list)):

            # `expandvars` is called, even though it currently
            # isn't necessary, so as to enable edits to the above
            # `environ` that reference system environment variables,
            # without changing the logic of the below.
            [env[key].append(expandvars(v)) for v in value]
        else:
            env[key] = expandvars(value)
