name = "rezutils"
version = "1.0"


def commands():
    global env
    env["PYTHONPATH"].prepend("{root}/python")
