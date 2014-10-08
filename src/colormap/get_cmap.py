# -*- python -*-
#
#  This file is part of colormap software
#
#  Copyright (c) 2014L
#
#  File author(s): Thomas Cokelaer <cokelaer@gmail.com>
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: 
#
##############################################################################
from colormap import Colormap

__all__ = ['get_cmap', 'cmap_builder']


def get_cmap(name, name2=None, name3=None):
    print("Deprecated. please use cmap_builder function instead")
    return get_cmap(name, name2, name3)

def cmap_builder(name, name2=None, name3=None):
    """return a registered colormap

    Valid name are those from matplotlib and **heat** (same as in R)
    """
    c = Colormap()
    # an R colormap
    if name and name2 and name3:
        return c.cmap_linear(name, name2, name3)
    elif name and name2:
        return c.cmap_bicolor(name, name2)
    elif name == 'heat':
        return c.get_cmap_heat()
    elif name == 'heat_r':
        return c.get_cmap_heat_r()
    # matplotlic colormaps
    elif name in c.colormaps:
        return c.cmap(name)
    # some custom diverging colormaps with black in the middle.
    elif name in c.diverging_black:
        return c.cmap(name)
    else:
        raise ValueError("name provided {0} is not recognised. ".format(name))

