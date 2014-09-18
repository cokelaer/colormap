
Installation
###################

Prerequisites
===============

You will need to install `Python <http://www.python.org/download/>`_
(linux and mac users should have it installed already). We recommend also to install `ipython <http://ipython.org/>`_, which provides a more flexible shell alternative to the python shell itself. **colormap** requires matplotlib and **easydev**, which are available on pypi and installed automatically with this package.

Installation
================
Since **colormap** is available on `PyPi <http://pypi.python.org/colormap>`_, the following command should install the package and its dependencies automatically:: 

    pip install colormap

Example
##########

Create your own colormap from red to green colors with intermediate color as
whitish (diverging map from red to green)::

    c = Colormap()
    mycmap = c.cmap( {'red':[1,1,0], 'green':[0,1,.39],  'blue':[0,1,0]})
    c.test_colormap(mycmap)

See user guide for details.


User guide
##################


.. toctree::
    :maxdepth: 2
    :numbered:

    quickstart.rst

Reference Guide
##################


.. toctree::
    :maxdepth: 2
    :numbered:

    references

