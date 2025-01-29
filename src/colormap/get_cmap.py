# -*- python -*-
#
#  This file is part of colormap software
#
#  Copyright (c) 2011-2024
#
#  File author(s): Thomas Cokelaer <cokelaer@gmail.com>
#
#  Distributed under the terms of the 3-clause BSD license.
#  The full license is in the LICENSE file, distributed with this software.
#
##############################################################################
from colormap import Colormap

__all__ = ["cmap_builder"]


def cmap_builder(name, name2=None, name3=None):
    """return a colormap object compatible with matplotlib

    If only parameter **name** is provided, it should be a known matplotlib
    colormap name (e.g., jet). If **name2** is provided, then a new colormap
    is created going from the color **name** to the color **name2** with a
    linear scale. Finally, if **name3** is provided, a linear scaled colormap
    is built from color **name** to color **name3** with the intermediate color
    being the **name2**

    Matplotlib colormap map names

    """
    c = Colormap()

    # if the colormap is already a colormap, nothing to do
    try:  # pragma: no cover
        name.get_bad()
        return name
    except AttributeError:
        pass

    # an R colormap
    if name and name2 and name3:
        return c.cmap_linear(name, name2, name3)
    elif name and name2:
        return c.cmap_bicolor(name, name2)
    elif name == "heat":
        return c.get_cmap_heat()
    elif name == "heat_r":
        return c.get_cmap_heat_r()
    # matplotlic colormaps
    elif name in c.colormaps:
        return c.cmap(name)
    # some custom diverging colormaps with black in the middle.
    elif name in c.diverging_black:
        return c.cmap(name)
    elif name.count("_") == 2:  # pragma: no cover
        name1, name2, name3 = name.split("_")
        return c.cmap_linear(name1, name2, name3)
    else:
        # valid = c.colormaps + c.diverging_black
        txt = "name provided {0} is not recognised. ".format(name)
        txt += "\n valid name can be found in colormap.colormap_names"
        raise ValueError(txt)
