#!/usr/bin/env python


from GT import GTLibrary
from version import Version
from . import lib
from . import public
from . import utils

__version__ = Version


class GTTestLibrary(GTLibrary):
    """
    This test library provides some keywords to allow
    Performance Test from Robot Framework.

    This test library depend on Robot Framework.
    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = Version
