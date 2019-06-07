name = "rezutils"
version = "1.2.5"
category = "int"
requires = [
    "python-2.7",
]


def commands():
    global env
    env["PYTHONPATH"].prepend("{root}/python")
