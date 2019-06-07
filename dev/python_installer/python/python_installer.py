import os
import glob
import errno
import zipfile
import argparse

try:
    from urllib.request import urlretrieve
except ImportError:
    # Support for Python 2.7
    from urllib import urlretrieve


parser = argparse.ArgumentParser()
parser.add_argument("version", default="3.7.3")

opts = parser.parse_args()

path = (
    os.environ["REZ_BUILD_INSTALL_PATH"]
    if os.getenv("REZ_BUILD_INSTALL")
    else os.environ["REZ_BUILD_PATH"]
)

variants = os.environ["REZ_BUILD_VARIANT_REQUIRES"].split()


def win_64():
    url = "https://www.python.org/ftp/python/{0}/python-{0}-embed-amd64.zip"
    url = url.format(opts.version)
    dst = os.path.join(path, "python")
    fname = os.path.join(dst, os.path.basename(url))

    try:
        os.makedirs(dst)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    print("Downloading %s.." % url)
    urlretrieve(url, fname)

    print("Unzipping.. %s" % fname)
    with zipfile.ZipFile(fname) as f:
        f.extractall(dst)

    print("Cleaning up..")
    os.remove(fname)

    # These normally restrict Python from reading PYTHONPATH
    for pth in glob.glob(os.path.join(dst, "*._pth")):
        os.remove(pth)

    print("Done")


def linux_64():
    pass


if variants == ["platform-windows", "arch-AMD64"]:
    win_64()

elif variants == ["platform-linux", "arch-x84_64"]:
    linux_64()

else:
    raise OSError("Unsupported architecture, %s" % ", ".join(variants))
