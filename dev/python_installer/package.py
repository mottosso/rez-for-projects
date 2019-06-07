name = "python_installer"
version = "1.0.0"

build_command = "python -m rezutils build {root}"
private_build_requires = ["rezutils-1"]


def commands():
    global env
    env.PYTHONPATH.prepend("{root}/python")
