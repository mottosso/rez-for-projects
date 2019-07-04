name = "rezutil"
version = "1.3.1"
requires = [
    "python-2.7+,<4",
]

_category = "int"


def commands():
    global env
    env["PYTHONPATH"].prepend("{root}/python")
