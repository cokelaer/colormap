# -*- coding: utf-8 -*-
__revision__ = "$Id: setup.py 3170 2013-01-16 14:57:19Z cokelaer $"
import sys
import os
from setuptools import setup, find_packages
import glob

_MAJOR               = 1
_MINOR               = 0
_MICRO               = 1
version              = '%d.%d.%d' % (_MAJOR, _MINOR, _MICRO)
release              = '%d.%d' % (_MAJOR, _MINOR)

metainfo = {
    'authors': {'Cokelaer':('Thomas Cokelaer','cokelaer@ebi.ac.uk')},
    'version': version,
    'license' : 'LGPL',
    'download_url' : ['http://pypi.python.org/pypi/colormap'],
    'url' : ["http://packages.python.org/colormap/"],
    'description':'Utilities to ease manipulation of matplotlib colormaps and color codecs (e.g., hex2rgb)',
    'platforms' : ['Linux', 'Unix', 'MacOsX', 'Windows'],
    'keywords' : ["hex2web", "web2hex", "hex2rgb", "rgb2hex", "rgb2hsv", "hsv2rgb", 
        "rgb2hls", "hls2rgb", "colormap", 'colors'],
    'classifiers' : [
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Topic :: Software Development :: Libraries :: Python Modules'
          ]
    }


on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if on_rtd is True:  # only import and set the theme if we're building docs
    install_requires = ['matplotlib', 'easydev', "numpydoc"]
else:
    install_requires = ['matplotlib', 'easydev']



setup(
    name             = 'colormap',
    version          = version,
    maintainer       = metainfo['authors']['Cokelaer'][0],
    maintainer_email = metainfo['authors']['Cokelaer'][1],
    author           = metainfo['authors']['Cokelaer'][0],
    author_email     = metainfo['authors']['Cokelaer'][1],
    long_description = open("README.rst").read(),
    keywords         = metainfo['keywords'],
    description = metainfo['description'],
    license          = metainfo['license'],
    platforms        = metainfo['platforms'],
    url              = metainfo['url'],
    download_url     = metainfo['download_url'],
    classifiers      = metainfo['classifiers'],

    # package installation
    package_dir = {'':'src'},
    packages = ['colormap'],
    requires = install_requires,
)




