import os
import sys
import time
import errno
import shutil
import zipfile
import argparse
import tempfile
import subprocess

try:
    from urllib.request import urlretrieve
except ImportError:
    # Support for Python 2.7
    from urllib import urlretrieve

parser = argparse.ArgumentParser()
parser.add_argument("root")
parser.add_argument("version")
parser.add_argument("--overwrite", action="store_true")
parser.add_argument("--bucket", action="append", metavar=(
    "https://github.com/.../master.zip"), help=(
    "URLs to included buckets, compatible with this "
    "exact version of Scoop"
))

opts = parser.parse_args()


def ask(msg):
    try:
        raw_input
    except NameError:
        # Python 2 support
        raw_input = input

    try:
        value = raw_input(msg).lower().rstrip()  # account for /n and /r
        return value in ("", "y", "yes", "ok")
    except EOFError:
        return True  # On just hitting enter
    except KeyboardInterrupt:
        return False


if int(os.getenv("REZ_BUILD_INSTALL")):
    install_dir = os.environ["REZ_BUILD_INSTALL_PATH"]
    exists = os.path.exists(install_dir)

    if exists and os.listdir(install_dir):
        print("Previous install found %s" % install_dir)

        if opts.overwrite or ask("Overwrite existing install? [Y/n] "):
            print("Cleaning existing install %s.." % install_dir)
            assert subprocess.check_call(
                'rmdir /S /Q "%s"' % install_dir, shell=True
            ) == 0, "Failed"
        else:
            print("Aborted")
            exit(1)


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

    yield "Extracting %s.." % os.path.basename(repo)

    try:
        with zipfile.ZipFile(fname) as f:
            f.extractall(tempdir)
    except (zipfile.BadZipfile, IOError):
        print("FAILED: '%s' likely not found" % url)
        exit(1)

    # Inner directory formatted as `repo-branch`
    branch_dir = os.path.join(tempdir, "%s-%s" % (repo, branch))

    try:
        os.makedirs(os.path.dirname(dst))
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    shutil.copytree(branch_dir, dst)
    shutil.rmtree(tempdir)


build_dir = os.environ["REZ_BUILD_PATH"]
print("Building into: %s" % build_dir)

# SCOOP_HOME hierarchy
home_dir = os.path.join(build_dir, "home")
scoop_dir = os.path.join(home_dir, "apps", "scoop", "current")
buckets_dir = os.path.join(home_dir, "buckets")
cache_dir = os.path.join(home_dir, "cache")
shims_dir = os.path.join(home_dir, "shims")

# Download scoop
stages = 4 + len(opts.bucket)
width = 24
stepsize = width // stages
msg = "Installing scoopz [{:<%d}] ({}/{}) {}       \r" % width
data = {"stage": 1}


def step(status):
    progress = "=" * stepsize * data["stage"]
    sys.stdout.write(msg.format(progress, data["stage"], stages, status))
    data["stage"] += 1


version = opts.version.rsplit(".", 1)[0]  # Last digit is ours
version = version.replace(".", "-")  # Rez to GitHub tag
url = "https://github.com/lukesampson/scoop/archive/%s.zip" % version
for status in github_download(url, scoop_dir):
    step(status)

for url in opts.bucket:
    _, repo, _, _ = url.rsplit("/", 3)
    bucket_dir = os.path.join(buckets_dir, repo.lower())
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

# Crippe automatic updates
scoop_update_ps1 = os.path.join(scoop_dir, "libexec", "scoop-update.ps1")
scoop_status_ps1 = os.path.join(scoop_dir, "libexec", "scoop-status.ps1")

if not os.path.exists(scoop_update_ps1):
    print("WARNING: Couldn't disable Scoop's automatic updates, "
          "the resulting package may try and update itself.")

else:
    print("Disabling automatic updates")
    with open(scoop_update_ps1, "w") as f:
        f.write("exit 0\n")  # A winner every day!

    with open(scoop_status_ps1, "w") as f:
        f.write('success "Everything is ok!"\n')
        f.write('exit 0\n')

if int(os.getenv("REZ_BUILD_INSTALL")):
    patterns = shutil.ignore_patterns("*.pyc")

    try:
        shutil.rmtree(install_dir)  # Created by Rez
    except Exception:
        # May not exist
        pass

    shutil.copytree(build_dir, install_dir, ignore=patterns)

# Install
print("Success!")
time.sleep(0.2)
