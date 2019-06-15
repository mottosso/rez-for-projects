import os

# Destination paths, during `rez build --install` or `rez release`
# local_packages_path = os.getenv("REZ_LOCAL_PACKAGES_PATH", "~/packages")
release_packages_path = os.getenv("REZ_RELEASE_PACKAGES_PATH")

# assert local_packages_path, "Missing REZ_LOCAL_PACKAGES_PATH"
assert release_packages_path, "Missing REZ_RELEASE_PACKAGES_PATH"

# Subdirectories of packages_path
categories = ("int", "ext", "td", "proj", "app")

# Search path during `rez env`
packages_path = [
    os.path.join(release_packages_path, category)
    for category in categories
]

# Your rez-bind packages, like platform and os
packages_path.insert(0, os.path.expanduser("~/packages"))


def package_preprocess_function(this, data):
    from rez.package_py_utils import InvalidPackageError

    # Enable a package to override path from package.py
    try:
        # data["config"]["local_packages_path"]
        data["config"]["release_packages_path"]
    except KeyError:
        pass
    else:
        return

    try:
        category = data["_category"]
        assert category in categories

    except KeyError:
        raise InvalidPackageError(
            "%s did not provide a `_category`" % data["name"]
        )

    except AssertionError:
        raise InvalidPackageError(
            "%s was not one of: %s" % (category, ", ".join(categories))
        )

    config = data.get("config", {})

    config["release_packages_path"] = os.path.join(
        release_packages_path, "%s" % category
    )
    # config["local_packages_path"] = os.path.join(
    #     local_packages_path, "%s" % category
    # )

    data["config"] = config
