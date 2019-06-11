import os
import sys
import time
import shutil
import argparse
import contextlib
import subprocess
import collections

dirname = os.path.dirname(__file__)
repodir = os.path.dirname(dirname)

# Some packages are directly from pip
pip = [
    "Qt.py==1.1.0",
    "pyblish-base==1.7.2",
    "pyblish-lite==0.8.4",
    "pyblish-qml==1.9.9",
]

scoop = [
    "python",
]

# Some packages depend on other packages
# having been built first.
order = [
    "scoopz",
    "rezutils",
    "welcome",
    "ftrack",
    "gitlab",
    "base",
    "core_pipeline",
    "maya",
    "maya_base",
    "pip",
]


parser = argparse.ArgumentParser()
parser.add_argument("--verbose", action="store_true")
opts = parser.parse_args()


def call(command, **kwargs):
    popen = subprocess.Popen(
        command,
        shell=True,
        universal_newlines=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        **kwargs
    )

    output = list()
    for line in iter(popen.stdout.readline, ""):
        output += [line.rstrip()]

        if opts.verbose:
            sys.stdout.write(line)

    popen.wait()

    if popen.returncode != 0:
        raise OSError(
            # arg1, arg2 -------
            # Some error here
            # ------------------
            "\n".join([
                "%s ".ljust(70, "-") % ", ".join(command),
                "",
                "\n".join(output),
                "",
                "-" * 70,
            ])
        )


@contextlib.contextmanager
def stage(msg, timing=True):
    sys.stdout.write(msg)
    t0 = time.time()

    try:
        yield
    except Exception:
        print("fail")
        raise
    else:
        if timing:
            print("ok - %.2fs" % (time.time() - t0))
        else:
            print("ok")


print("-" * 30)
print("")
print("Auto-building..")
print("")
print("-" * 30)

repos = (
    "local_packages_path",
    "release_packages_path",
)

for repo in repos:
    path = os.path.join(repodir, repo)
    _, existing, _ = next(os.walk(path))  # just directories

    if existing:
        with stage("Cleaning %s.. " % repo):
            for attempt in range(3):
                try:
                    for package in existing:
                        shutil.rmtree(os.path.join(path, package))
                except OSError:
                    sys.stderr.write(" retrying..")
                    time.sleep(1)
                    continue
                else:
                    break

count = 0

with stage("Scanning.. "):
    root = os.path.join(repodir, "dev")
    packages = collections.defaultdict(list)
    for base, dirs, files in os.walk(root):

        for fname in files:
            if fname != "package.py":
                continue

            dirs[:] = []  # Stop traversing
            abspath = os.path.join(base, fname)

            with open(abspath) as f:
                for line in f:
                    if line.startswith("name"):
                        name = line.split(" = ")[-1]
                        name = name.rstrip()  # newline
                        name = name.replace("\"", "")  # quotes
                    if line.startswith("version"):
                        version = line.split(" = ")[-1]
                        version = version.rstrip()  # newline
                        version = version.replace("\"", "")  # quotes

            packages[name] += [{
                "name": name,
                "base": base,
                "version": version,
                "abspath": abspath,
            }]

# Order relevant packages by above criteria
with stage("Sorting.. "):
    sorted_packages = []
    for name in order:
        sorted_packages += packages.pop(name)

    # Add remainder
    for _, package in packages.items():
        sorted_packages += package

with stage("Building scoop.. "):
    scoopz = next(pkg for pkg in sorted_packages if pkg["name"] == "scoopz")
    sorted_packages.remove(scoopz)
    call("rez build --clean --install", cwd=scoopz["base"])
    count += 1

with stage("Scoop installing.. "):
    for package in scoop:
        print(" - %s" % package)
        call("rez env scoopz -- install %s -y" % package)
        count += 1

with stage("Building.. "):
    for package in sorted_packages:
        print(" - {name}-{version}".format(**package))
        call("rez build --clean --install", cwd=package["base"])
        count += 1

with stage("Pip installing.."):
    for package in pip:
        print(" - %s" % package)
        call("rez pip --install --release %s" % package)
        count += 1

print("-" * 30)
print("Auto-built %d packages for you" % count)
