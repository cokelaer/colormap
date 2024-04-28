# -*- python -*-
# -*- coding: utf-8 -*-
#
# This file is part of the colormap software
#
# Copyright (c) 2014
#
# File author(s): Thomas Cokelaer <cokelaer@gmail.com>
#
# Distributed under the GPLv3 License.
# See accompanying file LICENSE.txt or copy at
# http://www.gnu.org/licenses/gpl-3.0.html
#
# Website: https://www.github.com/cokelaer/colormap
# Documentation: http://packages.python.org/colormap
#
##############################################################################
"""main colormap module"""
from importlib import metadata


def get_package_version(package_name):
    try:
        version = metadata.version(package_name)
        return version
    except metadata.PackageNotFoundError:
        return f"{package_name} not found"


version = get_package_version("colormap")


from . import colors
from .colors import *
from .get_cmap import *
from .xfree86 import *

c = Colormap()
colormap_names = c.colormaps + c.diverging_black
# create an alias to test_colormap methiod
test_colormap = c.test_colormap
test_cmap = c.test_colormap
