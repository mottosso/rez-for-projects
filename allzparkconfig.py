import os

HERE = os.path.dirname(__file__)
PACKAGES = os.path.join(HERE, "packages")

projects = [
    "alita",
    "lotr",
    "panzerkunst",
    "spiderman",
    "vector",
    "hulk",
    "metroid",
]

applications = os.listdir(os.path.join(PACKAGES, "app"))


def metadata_from_package(package):
    data = getattr(package, "_data", {})

    data = {
        "label": data.get("label", package.name),
        "background": data.get("background"),
        "icon": data.get("icon", None),
        "hidden": data.get("hidden", False),
    }

    # Backwards compatibility
    backwards_icon = getattr(package, "_icons", {}).get("32x32")
    data["icon"] = data["icon"] or backwards_icon or ""

    return data
