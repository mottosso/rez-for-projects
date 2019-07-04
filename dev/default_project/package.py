name = "default_project"
version = "1.0.1"
requires = [
    "python",
]

build_command = "python -m rezutil build {root}"
private_build_requires = ["rezutil-1"]

category = "int"


def commands():
    global env
    global alias

    # For Windows
    env.PATH.prepend("{root}/bin")

    # For Unix
    alias("create", "python {root}/bin/create.py")
