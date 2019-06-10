import os
import sys
import time
import shutil
import zipfile
import argparse
import tempfile

try:
    from urllib.request import urlretrieve
except ImportError:
    # Support for Python 2.7
    from urllib import urlretrieve

parser = argparse.ArgumentParser()
parser.add_argument("root")
parser.add_argument("version")
parser.add_argument("bucket", help=(
    "Commit SHA to a specific bucket, compatible with this "
    "exact version of Scoop"
))

opts = parser.parse_args()

variants = os.environ["REZ_BUILD_VARIANT_REQUIRES"].split()

if variants != ["platform-windows", "arch-AMD64"]:
    raise OSError("scoopz only supported on 64-bit Windows")


def github_download(url, dst):
    yield "Downloading %s.." % os.path.basename(url)

    _, repo, _, branch = url.rsplit("/", 3)
    branch, _ = os.path.splitext(branch)

    tempdir = tempfile.mkdtemp()
    fname = os.path.join(tempdir, os.path.basename(url))
    urlretrieve(url, fname)

    yield "Extracting %s.." % os.path.basename(fname)

    try:
        with zipfile.ZipFile(fname) as f:
            f.extractall(tempdir)
    except (zipfile.BadZipfile, IOError):
        print("FAILED: '%s' likely not found" % url)
        exit(1)

    # Inner directory formatted as `repo-branch`
    branch_dir = os.path.join(tempdir, "%s-%s" % (repo, branch))
    os.makedirs(os.path.dirname(dst))
    shutil.copytree(branch_dir, dst)
    shutil.rmtree(tempdir)


build_dir = os.environ["REZ_BUILD_PATH"]
print("Building into: %s" % build_dir)

# SCOOP_HOME hierarchy
home_dir = os.path.join(build_dir, "home")
scoop_dir = os.path.join(home_dir, "apps", "scoop", "current")
bucket_dir = os.path.join(home_dir, "buckets", "main")
cache_dir = os.path.join(home_dir, "cache")
shims_dir = os.path.join(home_dir, "shims")

# Download scoop
stages = 4
width = 24
msg = "Installing scoopz [{:<%d}] ({}/4) {}       \r" % width
data = {"stage": 1, "stepsize": "=" * (width / stages)}


def step(status):
    progress = data["stepsize"] * data["stage"]
    sys.stdout.write(msg.format(progress, data["stage"], status))
    data["stage"] += 1


version = ".".join(opts.version.split(".")[:-1])  # Last digit is ours
version = version.replace(".", "-")  # Rez to GitHub tag
url = "https://github.com/lukesampson/scoop/archive/%s.zip" % version
for status in github_download(url, scoop_dir):
    step(status)

bucket = opts.bucket
url = "https://github.com/ScoopInstaller/Main/archive/%s.zip" % bucket
for status in github_download(url, bucket_dir):
    step(status)

sys.stdout.write("\n")

# Remaining empty dirs
os.makedirs(cache_dir)
os.makedirs(shims_dir)

# Our Rez files
shutil.copytree(
    os.path.join(opts.root, "bin"),
    os.path.join(build_dir, "bin")
)

shutil.copytree(
    os.path.join(opts.root, "python"),
    os.path.join(build_dir, "python")
)

if int(os.getenv("REZ_BUILD_INSTALL")):
    install_dir = os.environ["REZ_BUILD_INSTALL_PATH"]
    print("Installing to %s.." % install_dir)
    shutil.rmtree(install_dir)  # Created by Rez
    patterns = shutil.ignore_patterns("*.pyc")
    shutil.copytree(build_dir, install_dir, ignore=patterns)

# Crippe automatic updates
scoop_update_ps1 = os.path.join(scoop_dir, "libexec", "scoop-update.ps1")

if not os.path.exists(scoop_update_ps1):
    print("WARNING: Couldn't disable Scoop's automatic updates, "
          "the resulting package may try and update itself.")

else:
    print("Disabling automatic updates")
    with open(scoop_update_ps1, "w") as f:
        f.write("exit 0")  # A winner every day!

# Install
print("Success!")
time.sleep(0.2)
