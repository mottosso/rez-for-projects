name = "core_pipeline"
version = "2.1.0"
environ = {
    "PYTHONPATH": [
        "{root}/python",
    ],
}

private_build_requires = [
    "rezutils-1",
]


def commands():
    global env
    global this
    global system
    global expandvars

    for key, value in this.environ.items():
        if isinstance(value, (tuple, list)):
            [env[key].append(expandvars(v)) for v in value]
        else:
            env[key] = expandvars(value)
