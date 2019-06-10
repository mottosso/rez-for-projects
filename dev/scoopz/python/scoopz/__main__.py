import os
import sys
import time
import logging
import argparse
import traceback
import contextlib

from rez.config import config

from . import (
    lib,

    init,
    install,
    parse,
    deploy,
)

dirname = os.path.dirname
log = logging.getLogger(__name__)
quiet = {"": False}


def tell(msg, newlines=1):
    if quiet[""]:
        return

    sys.stdout.write("%s%s" % (msg, "\n" * newlines))


@contextlib.contextmanager
def stage(msg, timing=True):
    tell(msg, 0)
    t0 = time.time()

    try:
        yield
    except Exception:
        tell("fail")
        raise
    else:
        if timing:
            tell("ok - %.2fs" % (time.time() - t0))
        else:
            tell("ok")


def ask(msg):
    from rez.vendor.six.six.moves import input

    try:
        value = input(msg).lower().rstrip()  # account for /n and /r
        return value in ("", "y", "yes", "ok")
    except EOFError:
        return True  # On just hitting enter
    except KeyboardInterrupt:
        return False


def report(new, exists, destination):
    tell("The following NEW packages will be installed:")
    all_ = new + exists
    max_name = max((i.name for i in all_), key=len)
    max_version = max((str(i.version) for i in all_), key=len)
    row_line = "  {:<%d}{:<%d}{}" % (len(max_name) + 4, len(max_version) + 2)

    def format_variants(dist):
        return (
            "/".join(str(v) for v in dist.variants[0])
            if dist.variants else ""
        )

    for dist in new:
        tell(row_line.format(
            dist.name,
            dist.version,
            format_variants(dist)
        ))

    if exists:
        tell("The following packages will be SKIPPED:")
        for dist in exists:
            tell(row_line.format(
                dist.name,
                dist.version,
                format_variants(dist)
            ))

    size = sum(
        os.path.getsize(os.path.join(dirpath, filename))
        for dist in new
        for dirpath, dirnames, filenames in os.walk(dist.root)
        for filename in filenames
    ) / (10.0 ** 6)  # mb

    tell("Packages will be installed to %s" % destination)
    tell("After this operation, %.2f mb will be used." % size)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("request", help=(
        "Packages to install, e.g. python curl"))
    parser.add_argument("--verbose", action="store_true", help=(
        "Include Scoop output amongst scoopz messages."))
    parser.add_argument("--release", action="store_true", help=(
        "Write to REZ_RELEASE_PACKAGES_PATH"))
    parser.add_argument("--prefix", type=str, metavar="PATH", help=(
        "Write to this exact path"))
    parser.add_argument("-y", "--yes", action="store_true", help=(
        "Do not ask to install, just do it"))
    parser.add_argument("-q", "--quiet", action="store_true", help=(
        "Do not print anything to the console"))

    opts = parser.parse_args()
    opts.verbose = opts.verbose and not opts.quiet
    quiet[""] = opts.quiet

    logging.basicConfig(format="%(message)s")
    log.setLevel(
        logging.DEBUG
        if opts.verbose and not opts.quiet
        else logging.WARNING
    )

    packagesdir = opts.prefix or (
        config.release_packages_path if opts.release
        else config.local_packages_path
    )

    try:
        with stage("Initialising Scoop... "):
            home = init()

        with stage("Reading package lists... "):
            install(home, opts.request, verbose=opts.verbose)

        with stage("Parsing Scoop apps... "):
            distributions = parse(home)

        with stage("Discovering existing packages... "):
            new, exists = list(), list()
            for dist in distributions:

                # TODO: This does not take into account
                # non-filesystem packages of Rez.
                destination = os.path.join(
                    packagesdir,
                    dist.name,
                    dist.version,
                    *dist.variants[0]
                )

                if os.path.exists(destination):
                    exists += [dist]

                else:
                    new += [dist]

        if not new:
            for dist in exists:
                tell("%s was already installed" % dist)

            tell("No new packages were installed")
            exit(0)

        report(new, exists, packagesdir)

        if not opts.yes and not opts.quiet:
            if not ask("Do you want to continue? [Y/n] "):
                print("Aborted")
                exit(0)

        count = 0
        total = len(new)
        for index, dist in enumerate(new):
            msg = ("(%d/%d) Installing %s-%s.. " % (
                index + 1, total, dist.name, dist.version
            ))

            with stage(msg, timing=False):
                try:
                    deploy(dist, packagesdir)
                except Exception:
                    traceback.print_exc()
                else:
                    count += 1

        print("Successfully installed %d package%s" % (
            count, "s" if count else ""))

    finally:
        sys.stdout.write("Cleaning up.. ")
        lib.call('rmdir /S /Q "%s"' % home)
        print("ok")
