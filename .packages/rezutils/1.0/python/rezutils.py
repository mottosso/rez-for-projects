import os
import sys
import time
import errno
import shutil
import fnmatch

# Include all files from a package, except these
# Think of these as a `.gitignore`
IGNORE = [
    "package.py",
    "rezbuild.py",
    "build",

    ".git",
    "doc",
    "docs",
    "*.pyc",
    ".cache",
    "__pycache__",
    "*.pyproj",
    "*.sln",
    ".vs",
]

# IO is unreliable; in this script, we'll give
# it this many attempts before throwing our hands up
RETRY = 3


def retry(func):
    def decorator(*args, **kwargs):
        for retry in range(RETRY):
            try:
                return func(*args, **kwargs)
            except Exception:
                tell("Retrying..", 3)
                time.sleep(0.2 * retry + 0.2)
            else:
                break
        else:
            import traceback
            traceback.print_exc()
            raise Exception(
                "{func} was attempted {count} "
                "times, but failed".format(
                    func=func.__name__,
                    count=RETRY,
                ))

    return decorator


def tell(msg, level=0):
    sys.stdout.write(" " * level + msg + "\n")


def ignored(abspath):
    """Determine whether `abspath` should be excluded"""
    basename = os.path.basename(abspath)
    return any(
        fnmatch.filter([basename], i)
        for i in IGNORE
    )


@retry
def makedirs(path):
    dirname = os.path.dirname(path)

    try:
        os.makedirs(dirname)
    except OSError as e:
        if e.errno is errno.EEXIST:
            # Jobs already done
            return

        # Unexpected
        raise


def generate_manifest(root):
    for base, dirs, files in os.walk(root):
        if ignored(base):
            dirs[:] = []  # Don't continue down this hierarchy
            continue

        for fname in files:
            abspath = os.path.join(base, fname)
            relpath = os.path.relpath(abspath, root)

            if ignored(relpath):
                continue

            yield relpath


@retry
def clean(root):
    for base, dirs, files in os.walk(root):
        # All directories
        for dirname in dirs:
            abspath = os.path.join(base, dirname)
            tell("Removing dir %s" % dirname, 6)
            shutil.rmtree(abspath)

        # And files
        for fname in files:
            abspath = os.path.join(base, fname)
            tell("Removing file %s" % fname, 6)
            os.remove(abspath)


@retry
def copy_with_retry(src, dst):
    shutil.copyfile(src, dst)


def build(source_path, build_path, install_path, targets):
    manifest = list(generate_manifest(source_path))

    def _copy():
        if os.path.exists(build_path):
            tell("Cleaning previous build..", 3)
            clean(build_path)

        for relpath in manifest:
            tell("Writing %s" % relpath, 3)
            src = os.path.join(source_path, relpath)
            dst = os.path.join(build_path, relpath)
            makedirs(dst)
            copy_with_retry(src, dst)

    def _install():
        if os.path.exists(install_path):
            tell("Cleaning previous install..", 3)
            clean(install_path)

        for relpath in manifest:
            tell("Installing %s" % relpath, 3)
            src = os.path.join(build_path, relpath)
            dst = os.path.join(install_path, relpath)
            makedirs(dst)
            copy_with_retry(src, dst)

    _copy()

    if "install" in (targets or []):
        _install()
