from __future__ import print_function
from __future__ import division

import pkg_resources
try:
        version = pkg_resources.require("colormap")[0].version
        __version__ = version
except:
        version = ''


from .xfree86 import *

from . import colors
from .colors import *
