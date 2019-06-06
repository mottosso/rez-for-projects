# An example of how GitLab may be used to link every project
# at a given facility to its URI

name = "gitlab"
version = "1.1.2"
build_command = False
environ = {
    "GITLAB_URI": "https://gitlab.mycompany.co.jp",
}


def commands():
    import os
    global env
    global this
    global building

    if not building and "GITLAB_API_KEY" not in os.environ:
        print("WARNING: GITLAB_API_KEY missing")

    for key, value in this.environ.items():
        env[key] = value
