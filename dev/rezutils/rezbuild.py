import os
import sys

packagepy = os.getenv("REZ_BUILD_SOURCE_PATH")
pythonpath = os.path.join(packagepy, "python")
sys.path.insert(0, pythonpath)

from rezutils import _rezbuild
build = _rezbuild.build
