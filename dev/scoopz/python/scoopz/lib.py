import os
import sys
import json
import subprocess

from rez.utils.platform_ import platform_


def _rez_name(name):
    return name.replace("-", "_")


def call(command, **kwargs):
    verbose = kwargs.pop("verbose", False)

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

        if verbose:
            sys.stdout.write(line)

    popen.wait()

    if popen.returncode != 0:
        raise OSError(
            # scoop output -------
            # Some error here
            # ------------------
            "\n".join([
                "scoop output ".ljust(70, "-"),
                "",
                "\n".join(output),
                "",
                "-" * 70,
            ])
        )


def junction(src, dst):
    src, dst = map(os.path.abspath, [src, dst])

    # Directory symbolic link supports package residing
    # on network, but temporary installation directory
    # residing locally = optimal performance
    call('mklink /D "{dst}" "{src}"'.format(**locals()))


class Distribution(object):
    def __init__(self, home, name):
        name = _rez_name(name)

        self._name = name
        self._home = home
        self._path = os.path.join(home, "apps", name)

        # Every valid Scoop package has a version
        self._version = next(
            dirname for dirname in os.listdir(self._path)
            if dirname != "current"
        )

        # Full path to payload
        self._root = os.path.join(self._path, self._version)

        # Metadata is stored locally, as JSON documents
        fname = os.path.join(home, "buckets", "main", "bucket", name + ".json")
        with open(fname) as f:
            self._metadata = json.load(f)

    def __str__(self):
        return "%s-%s" % (self.name, self.version)

    def __repr__(self):
        return "Distribution('%s-%s', %r)" % (
            self._name, self._version, self._path
        )

    def files(self):
        abspath = os.path.join(self._path, self.version)
        for base, dirs, files in os.walk(abspath):
            for fname in files:
                yield os.path.join(base, fname)

    def binaries(self):
        executables = self._metadata.get("bin")

        if not executables:
            return

        # Exe may be either "file.exe" or ["fileA.exe", "fileB.exe"]
        if not isinstance(executables, (tuple, list)):
            executables = [executables]

        for exe in executables:

            # Exe may be either "file.exe" or ["file.exe", "alias", "arg1"]
            if not isinstance(exe, (tuple, list)):
                exe = [exe]

            fname = os.path.join(exe[0])

            try:
                alias = exe[1]
            except IndexError:
                alias = None

            try:
                args = exe[2:]
            except IndexError:
                args = []

            yield fname, alias, args

    @property
    def root(self):
        return self._root

    @property
    def url(self):
        try:
            return self._metadata["url"]
        except KeyError:
            arch = {
                "AMD64": "64bit",
                "i686": "32bit",
            }[platform_.arch]
            arch = self._metadata["architecture"][arch]

            # Spec says this attribute is mandatory, thus guaranteed
            return arch["url"]

    @property
    def description(self):
        return self._metadata.get("description", "")

    @property
    def requirements(self):
        depends = self._metadata.get("depends")

        if not depends:
            return []

        # Can be either string or list
        if not isinstance(depends, (tuple, list)):
            depends = [depends]

        return depends

    @property
    def variants(self):
        return [
            ["platform-%s" % platform_.name, "arch-%s" % platform_.arch]
        ]

    @property
    def path(self):
        return self._path

    @property
    def name(self):
        return self._name

    @property
    def version(self):
        return self._version
