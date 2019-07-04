import os

# Destination paths, during `rez build --install --release`
release_packages_path = os.path.join(os.path.dirname(__file__), "packages")

# Subdirectories of packages_path
categories = ("int", "ext", "td", "proj", "app")

# Search path during `rez env`
packages_path = [
    os.path.join(release_packages_path, category)
    for category in categories
]

# Your localised packages
packages_path.insert(0, os.path.expanduser("~/.packages"))

# Your development packages
packages_path.insert(0, os.path.expanduser("~/packages"))


def package_preprocess_function(this, data):
    from rez.package_py_utils import InvalidPackageError

    # Enable a package to override path from package.py
    try:
        data["config"]["release_packages_path"]
    except KeyError:
        pass
    else:
        return

    try:
        category = data["_category"]
        assert category in categories

    except KeyError:
        # Support for packages without categories,
        # assumed to be external.
        category = "ext"

    except AssertionError:
        raise InvalidPackageError(
            "%s was not one of: %s" % (category, ", ".join(categories))
        )

    config = data.get("config", {})

    config["release_packages_path"] = os.path.join(
        release_packages_path, "%s" % category
    )

    data["config"] = config


# These packages are typically overly specific to your platform
# These maps allow for e.g. `windows-10.0.1803` packages to run
# to run on `windows-10.0.1903`
platform_map = {
    "os": {

        # Technically, 6.2 is Windows 8, 6.1 is Windows 7
        r"windows-6(.*)": r"windows-10",

        r"windows-10(.*)": r"windows-10",
    },
}
