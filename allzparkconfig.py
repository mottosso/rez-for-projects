import os

from allzpark import allzparkconfig

HERE = os.path.dirname(__file__)
PACKAGES = os.path.join(HERE, "packages")

projects = os.listdir(os.path.join(PACKAGES, "proj"))
applications = os.listdir(os.path.join(PACKAGES, "app"))


def read_package_data(package):
    data = getattr(package, "_data", {})

    data = {
        "label": data.get("label", package.name),
        "background": data.get("background"),
        "icon": data.get("icon", None),
        "hidden": data.get("hidden", False),
    }

    # data = allzparkconfig._read_package_data(package)

    # Backwards compatibility
    backwards_icon = getattr(package, "_icons", {}).get("32x32")
    data["icon"] = data["icon"] or backwards_icon or ""

    return data
