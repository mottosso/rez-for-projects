import os
import shutil


def build(source_path, build_path, install_path, targets):
    src = os.path.join(source_path, "python", "rezutils.py")
    dst = os.path.join(build_path, "python", "rezutils.py")

    try:
        os.makedirs(os.path.dirname(dst))
    except OSError:
        pass

    shutil.copyfile(src, dst)

    if "install" in targets:
        src = os.path.join(build_path, "python", "rezutils.py")
        dst = os.path.join(install_path, "python", "rezutils.py")

        try:
            os.makedirs(os.path.dirname(dst))
        except OSError:
            pass

        shutil.copyfile(src, dst)
