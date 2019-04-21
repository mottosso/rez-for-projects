name = "rezutils"
version = "1.0"
requires = [
    "python>=2.7,<4",
]


def commands():
    global env
    env["PYTHONPATH"].prepend("{root}/python")
