import os
import sys
import errno
import argparse

try:
    # Python 2
    input = raw_input
except NameError:
    pass

this = os.path.dirname(__file__)
template_py = os.path.join(this, "..", "template.py")

parser = argparse.ArgumentParser(description="Create a new project")
parser.add_argument("name", help="Name of project")
parser.add_argument("-y", "--yes", action="store_true", help=(
    "Do not ask for confirmation, just do it."))
parser.add_argument("--version", default="1.0.0", help="Initial version")
parser.add_argument("--prefix", default=os.getcwd(), help=(
    "Where to write a new project"))

opts = parser.parse_args()


def ask(msg):
    try:
        # Python 2 support
        _input = raw_input
    except NameError:
        _input = input

    try:
        value = _input(msg).lower().rstrip()  # account for /n and /r
        return value in ("", "y", "yes", "ok")
    except EOFError:
        return True  # On just hitting enter
    except KeyboardInterrupt:
        return False


template = list()
with open(template_py) as f:
    for line in f:

        # Skip comments
        if line.strip().startswith("##"):
            continue

        template += [line]
template = "".join(template)


dirname = os.path.join(opts.prefix, opts.name)
package_py = os.path.join(dirname, "package.py")
exists = os.path.exists(package_py)
action = "Updating" if exists else "Creating"
question = "Overwrite? [Y/n] " if exists else "Continue? [Y/n] "
print(action + " \"%s\"" % dirname)

if opts.yes or ask(question):
    try:
        os.makedirs(dirname)
    except OSError as e:
        if e.errno != errno.EEXIST:
            sys.stderr.write("Could not create directory %s\n" % dirname)
            exit(1)

    try:
        with open(package_py, "w") as f:
            f.write(template % opts.__dict__)
    except OSError:
        sys.stderr.write("Could not write %s\n" % package_py)
        exit(1)

else:
    print("Aborted")
    exit(0)

print("Successfully %s %s" % ("updated" if exists else "created", dirname))
