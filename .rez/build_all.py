import os
import sys
import time
import shutil
import argparse
import subprocess
import collections

dirname = os.path.dirname(__file__)
repodir = os.path.dirname(dirname)

# Some packages depend on other packages
# having been built first.
order = [
    "python",
    "rezutils",
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

print("-" * 30)
print("")
print("Auto-building..")
print("")
print("-" * 30)

packagesdir = os.path.join(dirname, "packages")
_, existing, _ = next(os.walk(packagesdir))  # just directories

if existing:
    sys.stdout.write("Cleaning existing packages.. ")

    for attempt in range(3):
        try:
            for package in existing:
                shutil.rmtree(os.path.join(packagesdir, package))
        except OSError:
            print("Retrying..")
            time.sleep(1)
            continue
        else:
            break

    print("all clean")

count = 0

print("Scanning..")
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
print("Sorting..")
sorted_packages = []
for name in order:
    sorted_packages += packages.pop(name)

# Add remainder
for _, package in packages.items():
    sorted_packages += package


print("Building..")
for package in sorted_packages:
        print(" - {name}-{version}".format(**package))

        try:
            with open(os.devnull, "w") as devnull:
                subprocess.check_call(
                    "rez build --install",
                    cwd=package["base"],
                    shell=True,
                    stdout=None if opts.verbose else devnull,
                )

        except subprocess.CalledProcessError:
            raise

        count += 1

print("-" * 30)
print("Auto-built %d packages for you" % count)
