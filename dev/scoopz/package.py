import sys as _sys

name = "scoopz"
version = "2019.05.15.6"

# Each version of Scoop of heavily coupled with whatever its
# repository of available packages look like at the time. It
# is an informal relationship, enforced by Scoop's automatic
# update mechanism.
_buckets = {
    "main": (
        "https://github.com/ScoopInstaller/Main/archive/"
        "0dc4efce64c2e3ef2893e58a604663318dbbf65a.zip"
    ),
    "versions": (
        "https://github.com/ScoopInstaller/Versions/archive/"
        "7346b7d9676a5940a496ddb5f1844e85d9b9919a.zip"
    )
}

_category = "ext"

# Scoop cannot require Python, as Python is one of the
# things installed using Scoop. To address this, we leverage
# the Python install Rez is using, which is guaranteed to be
# either 2.7-3.7+
build_command = "%s {root}/install.py {root} %s" % (_sys.executable, version)
build_command += " --overwrite"
build_command += " --bucket %s" % _buckets["main"]
build_command += " --bucket %s" % _buckets["versions"]

variants = [
    ["platform-windows", "arch-AMD64"]
]


def commands():
    global env

    env.PATH.prepend("{root}/bin")
    env.PATH.prepend("{root}/home/apps/scoop/current/bin")  # Expose scoop.ps1
    env.PYTHONPATH.prepend("{root}/python")

    env.SCOOP = "{root}/home"
    env.SCOOP_HOME = "{root}/home"
