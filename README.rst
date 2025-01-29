#############################
COLORMAP documentation
#############################


Please see : http://colormap.readthedocs.io/ for an up-to-date documentation.

.. image:: https://badge.fury.io/py/colormap.svg
    :target: https://pypi.python.org/pypi/colormap

.. image:: https://github.com/cokelaer/colormap/actions/workflows/ci.yml/badge.svg?branch=main
    :target: https://github.com/cokelaer/colormap/actions/workflows/ci.yml

.. image:: https://coveralls.io/repos/cokelaer/colormap/badge.png?branch=main
    :target: https://coveralls.io/r/cokelaer/colormap?branch=main

.. image:: https://static.pepy.tech/personalized-badge/colormap?period=month&units=international_system&left_color=black&right_color=orange&left_text=Downloads
    :target: https://pepy.tech/project/colormap

.. image:: http://readthedocs.org/projects/colormap/badge/?version=main
    :target: http://colormap.readthedocs.org/en/latest/?badge=main
    :alt: Documentation Status




:version: Python 3.9, 3.10, 3.11, 3.12
:contributions: Please join https://github.com/cokelaer/colormap
:issues: Please use https://github.com/cokelaer/colormap/issues
:notebook: Please see https://github.com/cokelaer/colormap/tree/main/notebooks


What is it ?
################

**colormap** package provides utilities to convert colors between
RGB, HEX, HLS, HUV and a framework to easily create and build colormaps for matplotlib. All
matplotlib colormaps and some R colormaps are also available altogether. The
plot_colormap method (see below) is handy to quickly pick up a colormaps and
the test_colormap is useful to see a live version of the new colormap.


Installation
###################

::

    pip install colormap

Usage examples
###############

1. convert RGB to HEX:

::

    from colormap import rgb2hex, hex2rgb

    hex_color = rgb2hex(255, 0, 0)  # Red color in HEX
    print(hex_color)  # Output: "#ff0000"

    rgb_color = hex2rgb("#ff0000")  # Convert back to RGB
    print(rgb_color)  # Output: (255, 0, 0)

2. Generate a Custom colormap:

Create your own colormap. For instance, from red to green colors with intermediate color as
whitish (diverging map from red to green)::

      from colormap import Colormap
      c = Colormap()
      mycmap = c.cmap( {'red':[1,1,0], 'green':[0,1,.39], 'blue':[0,1,0]})
      cmap = c.test_colormap(mycmap)

Even simpler if the colormap is linear using color's name::

      from colormap import Colormap
      c = Colormap()
      mycmap = c.cmap_linear('red', 'white', 'green(w3c)')
      cmap = c.test_colormap(mycmap)

.. image:: https://colormap.readthedocs.io/en/latest/_images/quickstart-6.png
    :width: 50%
    :align: center

3. Visualise existing matplotlib colormap:

::

      from colormap import plot_colormap, plot_category
      plot_colormap("viridis")


Using the Colormap instance, you can see all valid names using::

      c.colormaps

Matplotlib is very well known in the PYthon ecosystem and has categorised colormaps into categories such as a
"diverging". To visualise all of them::

      plot_category('diverging')

.. image:: https://colormap.readthedocs.io/en/latest/_images/quickstart-4.png
    :width: 50%
    :align: center

Other sets of colormaps are : sequentials, sequentials2, misc, diverging, qualitative



See online documentation for details: http://colormap.readthedocs.io/

changelog
#########

========= ================================================================================
Version   Description
========= ================================================================================
1.3.0     * support for poetry 2.0 thanks to @cjwatson PR#26
          * Slightly better doc
1.2.0
1.1.0     * switch to pyproject. remove easydev dependency. compat for python 3.11 and
            3.12
1.0.6     * Fix a matplotlib deprecation
          * Fix RTD documentation
1.0.5     * remove Python3.6 and added Python3.10 to CI action
          * Fix issue in setup reported in https://github.com/cokelaer/colormap/pull/14
          * add requirements in MANIFEST
          * applied black on all files
========= ================================================================================
