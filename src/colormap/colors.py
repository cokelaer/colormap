# -*- python -*-
# -*- coding: utf-8 -*-
#
#  This file is part of the colormap software
#
#  Copyright (c) 2011-20134
#
#  File author(s): Thomas Cokelaer <cokelaer@gmail.com>
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  Website: https://github.com/cokelaer/colormap
#  Documentation: http://packages.python.org/colormap
#
##############################################################################
"""Utilities provided in this module can be found either in the
standard Python module called :mod:`colorsys` or in matplotlib.colors
(e.g rgb2hex) or are original to this module (e.g., rgb2huv)


"""
# matplotlib dependence is only inside Colormap class
import colorsys

from colormap.xfree86 import XFree86_colors

__all__ = [
    "HEX",
    "Color",
    "hex2web",
    "web2hex",
    "hex2rgb",
    "hex2dec",
    "rgb2hex",
    "rgb2hsv",
    "hsv2rgb",
    "rgb2hls",
    "hls2rgb",
    "yuv2rgb",
    "rgb2yuv",
    "to_intensity",
    "yuv2rgb_int",
    "rgb2yuv_int",
    "Colormap",
]


def check_range(data, dmin, dmax):
    if data < dmin or data > dmax:
        raise ValueError(f"Value must be in the range [{dmin}-{dmax}]. You provided {data}")


def swapdict(dic, check_ambiguity=True):
    """Swap keys for values in a dictionary

    ::

        >>> d = {'a':1}
        >>> swapdict(d)
        {1:'a'}

    """
    # this version is more elegant but slightly slower : return {v:k for k,v in dic.items()}
    if check_ambiguity:
        assert len(set(dic.keys())) == len(set(dic.values())), "values is not a set. ambiguities for keys."
    return dict(zip(dic.values(), dic.keys()))


def check_param_in_list(param, valid_values, name=None):
    """Checks that the value of param is amongst valid

    :param param: a parameter to be checked
    :param list valid_values: a list of values

    ::

        check_param_in_list(1, [1,2,3])
        check_param_in_list(mode, ["on", "off"])
    """
    if isinstance(valid_values, list) is False:

        raise TypeError(
            "the valid_values second argument must be a list of valid values. {0} was provided.".format(valid_values)
        )

    if param not in valid_values:
        if name:
            msg = "Incorrect value provided for {} ({})".format(name, param)
        else:
            msg = "Incorrect value provided (%s)" % param
        msg += "    Correct values are %s" % valid_values
        raise ValueError(msg)


def hex2web(hexa):
    """Convert hexadecimal string (6 digits) into *web* version (3 digits)

    .. doctest::

        >>> from colormap.colors import hex2web
        >>> hex2web("#FFAA11")
        '#FA1'

    .. seealso:: :func:`web2hex`, :func:`hex2rgb`
        :func:`rgb2hex`, :func:`rgb2hsv`, :func:`hsv2rgb`, :func:`rgb2hls`,
        :func:`hls2rgb`
    """
    hexa = HEX().get_standard_hex_color(hexa)
    return "#" + hexa[1::2]


def web2hex(web):
    """Convert *web* hexadecimal string (3 digits) into  6 digits version

    .. doctest::

        >>> from colormap.colors import web2hex
        >>> web2hex("#FA1")
        '#FFAA11'

    .. seealso:: :func:`hex2web`, :func:`hex2rgb`
        :func:`rgb2hex`, :func:`rgb2hsv`, :func:`hsv2rgb`, :func:`rgb2hls`,
        :func:`hls2rgb`
    """
    return HEX().get_standard_hex_color(web)


def hex2rgb(hexcolor, normalise=False):
    """This function converts a hex color triplet into RGB

    Valid hex code are:

     * #FFF
     * #0000FF
     * 0x0000FF
     * 0xFA1


    .. doctest::

        >>> from colormap.colors import hex2rgb
        >>> hex2rgb("#FFF", normalise=False)
        (255, 255, 255)
        >>> hex2rgb("#FFFFFF", normalise=True)
        (1.0, 1.0, 1.0)


    .. seealso:: :func:`hex2web`, :func:`web2hex`,
        :func:`rgb2hex`, :func:`rgb2hsv`, :func:`hsv2rgb`, :func:`rgb2hls`,
        :func:`hls2rgb`
    """
    hexcolor = HEX().get_standard_hex_color(hexcolor)[1:]
    r, g, b = int(hexcolor[0:2], 16), int(hexcolor[2:4], 16), int(hexcolor[4:6], 16)
    if normalise:
        r, g, b = _normalise(r, g, b)
    return r, g, b


def rgb2hex(r, g, b, normalised=False):
    """Convert RGB to hexadecimal color

    :param: can be a tuple/list/set of 3 values (R,G,B)
    :return: a hex vesion ofthe RGB 3-tuple

    .. doctest::

        >>> from colormap.colors import rgb2hex
        >>> rgb2hex(0,0,255, normalised=False)
        '#0000FF'
        >>> rgb2hex(0,0,1, normalised=True)
        '#0000FF'

    .. seealso:: :func:`hex2web`, :func:`web2hex`, :func:`hex2rgb`
        , :func:`rgb2hsv`, :func:`hsv2rgb`, :func:`rgb2hls`,
        :func:`hls2rgb`

    """
    if normalised:
        r, g, b = _denormalise(r, g, b, mode="rgb")
        r = int(r)
        g = int(g)
        b = int(b)

    check_range(r, 0, 255)
    check_range(g, 0, 255)
    check_range(b, 0, 255)

    return "#%02X%02X%02X" % (r, g, b)


def rgb2hls(r, g, b, normalised=True):
    """Convert an RGB value to an HLS value.

    :param bool normalised: if *normalised* is True, the input RGB triplet
        should be in the range 0-1 (0-255 otherwise)
    :return: the HLS triplet. If *normalised* parameter is True, the output
        triplet is in the range 0-1; otherwise, H in the range 0-360 and LS
        in the range 0-100.

    .. doctest::

        >>> from colormap.colors import rgb2hls
        >>> rgb2hls(255,255,255, normalised=False)
        (0.0, 1.0, 0.0)


    .. seealso:: :func:`hex2web`, :func:`web2hex`, :func:`hex2rgb`
        :func:`rgb2hex`, :func:`hsv2rgb`,
        :func:`hls2rgb`
    """
    # rgb_to_hsv expects normalised values !
    if normalised:
        upper = 1
    else:
        upper = 255
    check_range(r, 0, upper)
    check_range(g, 0, upper)
    check_range(b, 0, upper)
    if normalised == False:
        r, g, b = _normalise(r, g, b)
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return h, l, s


def rgb2hsv(r, g, b, normalised=True):
    """Convert an RGB value to an HSV value.

    :param bool normalised: if *normalised* is True, the input RGB triplet
        should be in the range 0-1 (0-255 otherwise)
    :return: the HSV triplet. If *normalised* parameter is True, the output
        triplet is in the range 0-1; otherwise, H in the range 0-360 and LS
        in the range 0-100.

    .. doctest::

        >>> from colormap.colors import rgb2hsv
        >>> rgb2hsv(0.5,0,1)
        (0.75, 1, 1)


    .. seealso:: :func:`hex2web`, :func:`web2hex`, :func:`hex2rgb`
        :func:`rgb2hex`, :func:`hsv2rgb`, :func:`rgb2hls`,
        :func:`hls2rgb`
    """
    # rgb_to_hsv expects normalised values !
    if normalised:
        upper = 1
    else:
        upper = 255
    check_range(r, 0, upper)
    check_range(g, 0, upper)
    check_range(b, 0, upper)
    if normalised == False:
        r, g, b = _normalise(r, g, b)
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    return h, s, v


def hsv2rgb(h, s, v, normalised=True):
    """Convert a hue-saturation-value (HSV) value to a red-green-blue (RGB).

    :param bool normalised: If *normalised* is True, the input HSV triplet
        should be in the range 0-1; otherwise, H in the range 0-360 and LS
        in the range 0-100.
    :return: the RGB triplet. The output
        triplet is in the range 0-1 whether the input is normalised or not.

    .. doctest::

        >>> from colormap.colors import hsv2rgb
        >>> hsv2rgb(0.5,1,1, normalised=True)  # doctest: +SKIP
        (0, 1, 1)


    .. seealso:: :func:`hex2web`, :func:`web2hex`, :func:`hex2rgb`
        :func:`rgb2hex`, :func:`rgb2hsv`, :func:`rgb2hls`,
        :func:`hls2rgb`
    .. seealso:: :func:`rgb2hex`
    """
    if normalised:
        upper = 1
    else:
        upper = 100
    if normalised:
        uppera = 1
    else:
        uppera = 360
    check_range(h, 0, uppera)
    check_range(s, 0, upper)
    check_range(v, 0, upper)
    if normalised == False:
        h, s, v = _normalise(h, s, v, mode="hsv")
    return colorsys.hsv_to_rgb(h, s, v)


def hls2rgb(h, l, s, normalised=True):
    """Convert an HLS value to a RGB value.

    :param bool normalised: If *normalised* is True, the input HLS triplet
        should be in the range 0-1; otherwise, H in the range 0-360 and LS
        in the range 0-100.

    :return: the RGB triplet. The output
        triplet is in the range 0-1 whether the input is normalised or not.

    .. doctest::

        >>> from colormap.colors import hls2rgb
        >>> hls2rgb(360, 50, 60, normalised=False)  # doctest: +SKIP
        (0.8, 0.2, 0.2)


    .. seealso:: :func:`hex2web`, :func:`web2hex`, :func:`hex2rgb`
        :func:`rgb2hex`, :func:`rgb2hsv`, :func:`hsv2rgb`, :func:`rgb2hls`,

    """
    if normalised:
        upper = 1
    else:
        upper = 100
    if normalised:
        uppera = 1
    else:
        uppera = 360
    check_range(h, 0, uppera)
    check_range(s, 0, upper)
    check_range(l, 0, upper)
    if normalised == False:
        h, l, s = _normalise(h, l, s, mode="hls")
    return colorsys.hls_to_rgb(h, l, s)


def hex2dec(data):
    """convert hexadecimal string (data) into a float in the [0-65536] inclusive range"""
    if data[0] == "#":
        data.replace("#", "")
    return int(data, 16) / 255


def rgb2yuv(r, g, b):
    """Convert RGB triplet into YUV

    :return: YUV triplet with values between 0 and 1

    `YUV wikipedia <http://en.wikipedia.org/wiki/YUV>`_

    .. warning:: expected input must be between 0 and 1
    .. note:: the constants referenc used is  Rec. 601
    """
    check_range(r, 0, 1)
    check_range(g, 0, 1)
    check_range(b, 0, 1)

    # y = int(0.299 * r + 0.587 * g + 0.114 * b)
    # u = int(-0.14713 * r + -0.28886 * g + 0.436 * b)
    # v = int(0.615 * r + -0.51499 * g + -0.10001 * b)

    y = 0.299 * r + 0.587 * g + 0.114 * b
    u = -32591 / 221500 * r + -63983 / 221500 * g + 0.436 * b
    v = 0.615 * r + -72201 / 140200 * g + -7011 / 70100 * b
    return (y, u, v)


def yuv2rgb(y, u, v):
    """Convert YUV triplet into RGB

    `YUV <http://en.wikipedia.org/wiki/YUV>`_

    .. warning:: expected input must be between 0 and 255 (not normalised)

    """
    check_range(y, 0, 1)
    check_range(u, 0, 1)
    check_range(v, 0, 1)
    A, B, C, D = 701 / 615, 25251 / 63983, 209599 / 361005, 443 / 218
    r = y + A * v
    g = y - B * u - C * v
    b = y + D * u
    return (r, g, b)


def rgb2yuv_int(r, g, b):
    """Convert RGB triplet into YUV

    `YUV wikipedia <http://en.wikipedia.org/wiki/YUV>`_

    .. warning:: expected input must be between 0 and 255 (not normalised)

    """
    check_range(r, 0, 255)
    check_range(g, 0, 255)
    check_range(b, 0, 255)

    y = int(0.299 * r + 0.587 * g + 0.114 * b)
    u = int(-32591 / 221500 * r + -63983 / 221500 * g + 0.436 * b)
    v = int(0.615 * r + -72201 / 140200 * g + -7011 / 70100 * b)

    return (y, u, v)


def yuv2rgb_int(y, u, v):
    """Convert YUV triplet into RGB

    `YUV <http://en.wikipedia.org/wiki/YUV>`_

    .. warning:: expected input must be between 0 and 255 (not normalised)

    """
    check_range(y, 0, 255)
    check_range(u, 0, 255)
    check_range(v, 0, 255)
    r = int(y + 1.13983 * v)
    g = int(y - 0.39465 * u - 0.58060 * v)
    b = int(y + 2.03211 * u)
    return (r, g, b)


def _denormalise(r, g, b, mode="rgb"):
    check_param_in_list(mode, ["rgb", "hls", "hsv"])
    if mode == "rgb":
        return r * 255, g * 255, b * 255
    elif mode in ["hls", "hsv"]:
        return r * 360, g * 100, b * 100


def _normalise(r, g, b, mode="rgb"):
    check_param_in_list(mode, ["rgb", "hls", "hsv"])
    if mode == "rgb":
        return r / 255, g / 255, b / 255
    elif mode in ["hls", "hsv"]:
        return r / 360, g / 100, b / 100


def to_intensity(n):
    """Return intensity

    :param n: value between 0 and 1
    :return: value between 0 and 255; round(n*127.5+127.5)
    """
    check_range(n, 0, 1)
    return round(n * 127.5 + 127.5)


class HEX(object):
    """Class to check the validity of an hexadecimal string and get standard string

    By standard, we mean #FFFFFF (6 digits)

    ::

        >>> h = HEX()
        >>> h.is_valid_hex_color("#FFFF00")
        True

    """

    def __init__(self):
        pass

    def is_valid_hex_color(self, value, verbose=True):
        """Return True is the string can be interpreted as hexadecimal color

        Valid formats are

         * #FFF
         * #0000FF
         * 0x0000FF
         * 0xFA1
        """
        try:
            self.get_standard_hex_color(value)
            return True
        except Exception as err:
            if verbose:
                print(err)
            return False

    def get_standard_hex_color(self, value):
        """Return standard hexadecimal color

        By standard, we mean a string that starts with # sign followed by 6
        character, e.g. #AABBFF
        """
        if isinstance(value, str) == False:
            raise TypeError("value must be a string")
        if len(value) <= 3:
            raise ValueError("input string must be of type 0xFFF, 0xFFFFFF or #FFF or #FFFFFF")

        if value.startswith("0x") or value.startswith("0X"):
            value = value[2:]
        elif value.startswith("#"):
            value = value[1:]
        else:
            raise ValueError("hexa string must start with a '#' sign or '0x' string")
        value = value.upper()
        # Now, we have either FFFFFF or FFF
        # now check the length
        for x in value:
            if x not in "0123456789ABCDEF":
                raise ValueError("Found invalid hexa character {0}".format(x))

        if len(value) == 6 or len(value) == 8:
            value = "#" + value[0:6]
        elif len(value) == 3:
            value = "#" + value[0] * 2 + value[1] * 2 + value[2] * 2
        else:
            raise ValueError("hexa string should be 3, 6 or 8 digits. if 8 digits, last 2 are ignored")
        return value


class Color(HEX):
    """Class to ease manipulation and conversion between color codes

    You can create an instance in many differen ways. You can either use a
    human-readable name as long as it is part of the
    `XFree86 list <http://en.wikipedia.org/wiki/X11_color_names>`_
    You can also provide a hexadecimal string (either 3 or 6 digits). You can
    use triplets of values corresponding to the RGB, HSV or HLS conventions.

    Here are some examples:

    .. doctest::

        from colormap import Color

        Color("red")           # human XFree86 compatible representation
        Color("#f00")          # standard 3 hex digits
        Color("#ff0000")       # standard 6 hex digits
        Color(hsv=(0,1,0.5))
        Color(hls=(0, 1, 0.5)) # HLS triplet
        Color(rgb=(1, 0, 0))   # RGB triplet
        Color(Color("red"))    # using an instance of :class:`Color`

    Note that the RGB, HLS and HSV triplets use normalised values. If you need
    to normalise the triplet, you can use :mod:`colormap.colors._normalise` that
    provides a function to normalise RGB, HLS and HSV triplets::

        colors._normalise(*(255, 255, 0), mode="rgb")
        colors._normalise(*(360, 50, 100), mode="hls")

    If you provide a string, it has to be a valid string from XFree86.
    In addition to the official names, the lower case names are valid. Besides,
    there are names with spaces. The equivalent names without space are also
    valid. Therefore the name "Spring Green", which is an official name can be
    provided as "Spring Green", "spring green", "springgreen" or "SpringGreen".

    """

    # Get official color names
    colors = XFree86_colors.copy()
    # add color names without spaces
    aliases = dict([(x.replace(" ", ""), x) for x in colors.keys() if " " in x])
    # add color names without spaces in lower cases
    aliases.update([(x.replace(" ", "").lower(), x) for x in colors.keys() if " " in x])
    # add color names in lower case
    aliases.update(dict([(x.lower(), x) for x in colors.keys()]))
    aliases.update(dict([(x, x) for x in colors.keys()]))

    # keep track of all possible names
    color_names = sorted(list(set(list(colors.keys()) + list(aliases.keys()))))

    def __init__(self, name=None, rgb=None, hls=None, hsv=None):
        super(Color, self).__init__()
        self._name = None
        self._mode = None
        self._rgb = None

        # Does the user provided the name argument (first one) as a string ?
        if isinstance(name, str):
            # if so, it can be a valid human name (e.g., red) or an hex
            # assuming that valid hexadecimal starts with # or 0x,
            # if we can interpret the string as an hexadecimal, we are done
            if self.is_valid_hex_color(name, verbose=False):
                self.hex = name
            else:
                # if not, then, the user probably provided a valid color name
                # the property will check the validity.
                self.name = name[:]
                # all other input parameters are ignored
        elif name == None:
            if rgb:
                self.rgb = rgb
            elif hls:
                self.hls = hls
            elif hsv:
                self.hsv = hsv
            else:
                raise ValueError("You must set one of the parameter")
        elif isinstance(name, Color):
            self.rgb = name.rgb
        else:
            raise ValueError("name parameter must be a string")

    def _get_name(self):
        return self._name

    def _set_name(self, name):
        check_param_in_list(name, self.color_names)
        name = self.aliases[name]
        self._name = name
        # set hex and rgb at the same time based on the name
        self.hex = self.colors[name]

    name = property(_get_name, _set_name)
    color = property(_get_name, _set_name)

    def _get_hex(self):
        return self._hex

    def _set_hex(self, value):
        # hex is an approximation made of 255 bits so do not define rgb here
        if self.is_valid_hex_color(value):
            value = self.get_standard_hex_color(value)
            self._hex = value
            if self._hex in self.colors.values():
                self._name = swapdict(self.colors, check_ambiguity=False)[self._hex]
            else:
                self._name = "undefined"
            self._rgb = hex2rgb(self._hex, normalise=True)
        else:
            # just to warn the user
            self.get_standard_hex_color(value)

    hex = property(_get_hex, _set_hex, doc="getter/setter the hexadecimal value.")

    def _get_rgb(self):
        return self._rgb

    def _set_rgb(self, value):
        # set name, hex and rgb
        self.hex = rgb2hex(*value, normalised=True)
        # must reset rgb with its real value (set_hex may round the rgb)
        # in _set_hex
        self._rgb = value

    rgb = property(_get_rgb, _set_rgb, doc="getter/setter the RGB values (3-length tuple)")

    def _get_hsv(self):
        hsv = rgb2hsv(*self.rgb)
        return hsv

    def _set_hsv(self, value):
        # TODO: value must be normalised
        self.rgb = hsv2rgb(*value)

    hsv = property(_get_hsv, _set_hsv, doc="getter/setter the HSV values (3-length tuple)")

    def _get_hls(self):
        hls = rgb2hls(*self.rgb)
        return hls

    def _set_hls(self, value):
        # hls = _normalise(*value, mode="hls")
        # else:
        hls = value
        self.rgb = hls2rgb(*hls)

    hls = property(_get_hls, _set_hls, doc="getter/setter the HLS values (3-length tuple)")

    def _get_lightness(self):
        return self.hls[1]

    def _set_lightness(self, lightness):
        h, l, s = self.hls
        self.hls = (h, lightness, s)

    lightness = property(_get_lightness, _set_lightness, doc="getter/setter the lightness in the HLS triplet")

    def _get_saturation_hls(self):
        return self.hls[2]

    def _set_saturation_hls(self, saturation):
        h, l, s = self.hls
        self.hls = (h, l, saturation)

    saturation_hls = property(
        _get_saturation_hls, _set_saturation_hls, doc="getter/setter the saturation in the HLS triplet"
    )

    def _get_hue(self):
        return self.hls[0]

    def _set_hue(self, hue):
        h, l, s = self.hls
        self.hls = (hue, l, s)

    hue = property(_get_hue, _set_hue, doc="getter/setter the saturation in the HLS triplet")

    def _get_red(self):
        return self.rgb[0]

    def _set_red(self, red):
        r, g, b = self.rgb
        self.rgb = (red, g, b)

    red = property(_get_red, _set_red, doc="getter/setter for the red color in RGB triplet")

    def _get_green(self):
        return self.rgb[1]

    def _set_green(self, green):
        r, g, b = self.rgb
        self.rgb = (r, green, b)

    green = property(_get_green, _set_green, doc="getter/setter for the green color in RGB triplet")

    def _get_blue(self):
        return self.rgb[2]

    def _set_blue(self, blue):
        r, g, b = self.rgb
        self.rgb = (r, g, blue)

    blue = property(_get_blue, _set_blue, doc="getter/setter for the blue color in RGB triplet")

    def _get_value(self):
        return self.hsv[2]

    def _set_value(self, value):
        h, s, v = self.hsv
        self.hsv = (h, s, value)

    value = property(_get_value, _set_value, doc="getter/setter the value in the HSV triplet")

    def _get_yiq(self):
        return colorsys.rgb_to_yiq(*self.rgb)

    yiq = property(_get_yiq, doc="Getter for the YIQ triplet")

    def __str__(self):
        txt = "Color {0}\n".format(self.name)
        txt += "  hexa code: {0}\n".format(self.hex)
        txt += "  RGB code: {0}\n".format(self.rgb)
        txt += "  RGB code (un-normalised): {0}\n\n".format([x * 255 for x in self.rgb])
        txt += "  HSV code: {0}\n".format(self.hsv)
        txt += "  HSV code: (un-normalised) {0} {1} {2}\n\n".format(
            self.hsv[0] * 360, self.hsv[1] * 100, self.hsv[2] * 100
        )
        txt += "  HLS code: {0}\n".format(self.hls)
        txt += "  HLS code: (un-normalised) {0} {1} {2}\n\n".format(
            self.hls[0] * 360, self.hls[1] * 100, self.hls[2] * 100
        )
        return txt


class Colormap(object):
    """Class to create matplotlib colormap

    This example show how to get the pre-defined colormap called *heat*

    .. plot::
        :include-source:


        from pylab import *
        from colormap.colors import Colormap

        c = Colormap()
        cmap = c.get_cmap_heat()
        c.test_colormap(cmap)

    You may be more interested in building your own colormap::

        # design your own colormap
        d = {'blue': [0,0,0,1,1,1,0],
                'green':[0,1,1,1,0,0,0],
                'red':  [1,1,0,0,0,1,1]}
        cmap = c.cmap(d, reverse=False)

        # see the results
        c.test_colormap(cmap)

    If you want a simple linear colormap, you can use the example above,
    or use the :meth:`cmap_linear`. For instance for a diverging colormap
    from red to green (with with color in between)::

        cmap = c.cmap_linear("red", "white", "green")
        c.test_colormap(cmap)

    Even simpler, you can use a bicolor colormap :meth:`cmap_bicolor`. For instance
    for a red to green colormap::

        cmap = c.cmap_bicolor("red", "green")
        c.test_colormap(cmap)

    From matplotlib documentation, colormaps falls into 4 categories:

    #. Sequential schemes for unipolar data that progresses from low to high
    #. Diverging schemes for bipolar data that emphasizes positive or
       negative deviations from acentral value
    #. Cyclic schemes  meant for plotting values that wrap around at the
       endpoints, such as phase angle, wind direction, or time of day
    #. Qualitative schemes for nominal data that has no inherent ordering,
       where color is used only to distinguish categories


    :references: matplotlib documentation and examples
        http://matplotlib.org/examples/color/colormaps_reference.html
    """

    def _get_colormap_mpl(self):
        try:
            from matplotlib.pyplot import colormaps as _cmaps

            return _cmaps()
        except:
            return []

    colormaps = property(_get_colormap_mpl)

    def _get_sequentials(self):
        return [
            "Blues",
            "BuGn",
            "BuPu",
            "GnBu",
            "Greens",
            "Greys",
            "OrRd",
            "Oranges",
            "PuBu",
            "PuBuGn",
            "PuRd",
            "Purples",
            "RdPu",
            "Reds",
            "YlGn",
            "YlGnBu",
            "YlOrBr",
            "YlOrRd",
        ]

    sequentials = property(_get_sequentials)

    def _get_sequentials2(self):
        return [
            "afmhot",
            "autumn",
            "bone",
            "cool",
            "copper",
            "gist_heat",
            "gray",
            "hot",
            "pink",
            "spring",
            "summer",
            "winter",
        ]

    sequentials2 = property(_get_sequentials2)

    def _get_diverging(self):
        return [
            "BrBG",
            "PRGn",
            "PiYG",
            "PuOr",
            "RdBu",
            "RdGy",
            "RdYlBu",
            "RdYlGn",
            "Spectral",
            "bwr",
            "coolwarm",
            "seismic",
        ]

    diverging = property(_get_diverging)

    def _get_diverging_black(self):
        return [
            "red_black_sky",
            "red_black_blue",
            "red_black_green",
            "yellow_black_blue",
            "yellow_black_sky",
            "red_black_orange",
            "pink_black_green(w3c)",
        ]

    diverging_black = property(_get_diverging_black)

    def _get_qualitative(self):
        return ["Accent", "Dark2", "Paired", "Pastel1", "Pastel2", "Set1", "Set2", "Set3"]

    qualitative = property(_get_qualitative)

    def _get_misc(self):
        return [
            "gist_earth",
            "terrain",
            "ocean",
            "gist_stern",
            "brg",
            "CMRmap",
            "cubehelix",
            "gnuplot",
            "gnuplot2",
            "gist_ncar",
            "nipy_spectral",
            "jet",
            "rainbow",
            "gist_rainbow",
            "hsv",
            "flag",
            "prism",
        ]

    misc = property(_get_misc)

    def plot_rgb_from_hex_list(self, cols):
        """This functions takes a list of hexadecimal values and plots
        the RGB curves. This can be handy to figure out the RGB functions
        to be used in the :meth:`get_cmap`.

        .. plot::
            :include-source:
            :width: 60%

            from colormap.colors import Colormap
            c = Colormap()
            t = ['#FF0000FF', '#FF4D00FF', '#FF9900FF', '#FFE500FF',
                 '#CCFF00FF', '#80FF00FF', '#33FF00FF', '#00FF19FF',
                 '#00FF66FF', '#00FFB2FF', '#00FFFFFF', '#00B3FFFF',
                 '#0066FFFF', '#001AFFFF', '#3300FFFF', '#7F00FFFF',
                 '#CC00FFFF','#FF00E6FF','#FF0099FF', '#FF004DFF']
            c.plot_rgb_from_hex_list(t)

        """
        import pylab

        red = [hex2rgb(x)[0] / 255 for x in cols]
        blue = [hex2rgb(x)[2] / 255 for x in cols]
        green = [hex2rgb(x)[1] / 255 for x in cols]
        x = pylab.linspace(0, 1, len(cols))
        pylab.clf()
        pylab.plot(x, red, "ro-", alpha=0.5)
        pylab.plot(x, green, "gs-", alpha=0.5, markersize=15)
        pylab.plot(x, blue, "bx-", alpha=0.5, markersize=15)
        pylab.ylim([-0.1, 1.1])

    def cmap_bicolor(self, color1, color2, reverse=False, N=256):
        """Provide 3 colors in format accepted by :class:`Color`

        ::

            >>> red = Color('red')
            >>> white = Color('white')
            >>> cmap = cmap_bicolor(red, white)

        """
        c1 = Color(color1)
        c2 = Color(color2)
        dico = {"red": [c1.red, c2.red], "green": [c1.green, c2.green], "blue": [c1.blue, c2.blue]}
        return self.cmap(dico, reverse=reverse, N=N)

    def cmap_linear(self, color1, color2, color3, reverse=False, N=256):
        """Provide 3 colors in format accepted by :class:`Color`

        ::

            red = Color('red')
            cmap = cmap_linear(red, 'white', '#0000FF')

        """
        c1 = Color(color1)
        c2 = Color(color2)
        c3 = Color(color3)
        dico = {
            "red": [c1.red, c2.red, c3.red],
            "green": [c1.green, c2.green, c3.green],
            "blue": [c1.blue, c2.blue, c3.blue],
        }

        return self.cmap(dico, reverse=reverse, N=N)

    def cmap(self, colors=None, reverse=False, N=256):
        """Return a colormap object to be used within matplotlib

        :param dict colors: a dictionary that defines the RGB colors to be
            used in the colormap. See :meth:`get_cmap_heat` for an example.
        :param bool reverse: reverse the colormap is  set to True (defaults to False)
        :param int N: Defaults to 50

        """
        # matplotlib colormaps
        if colors in self.colormaps:
            if reverse and colors.endswith("_r") is False:
                colors += "_r"
            from matplotlib import colormaps

            return colormaps[colors]
        # custom ones
        elif colors in self.diverging_black:
            c1, c2, c3 = colors.split("_")
            # special case of sky, which does not exists
            c3 = c3.replace("sky", "deep sky blue")
            return self.cmap_linear(c1, c2, c3)
        elif colors == "heat":
            return self.get_cmap_heat()
        elif colors == "heat_r":
            return self.get_cmap_heat_r()

        # Keep these dependencies inside the function to allow
        # installation of colormap without those dependencies
        # FIXME remove numpy dependencies
        import numpy as np

        # extracted from R, heat.colors(20)

        if reverse:
            for k in colors.keys():
                colors[k].reverse()

        # If index not given, RGB colors are evenly-spaced in colormap.
        index = np.linspace(0, 1, len(colors["red"]))

        # Adapt color_data to the form expected by LinearSegmentedColormap.
        color_data = dict((key, [(x, y, y) for x, y in zip(index, value)]) for key, value in list(colors.items()))

        import matplotlib

        f = matplotlib.colors.LinearSegmentedColormap
        m = f("my_color_map", color_data, N)
        return m

    def get_cmap_heat(self):
        """Return a heat colormap matplotlib-compatible colormap

        This heat colormap should be equivalent to heat.colors() in R.

        ::

            >>> from colormap.colors import Colormap
            >>> cmap = Colormap.get_cmap_heat()

        You can generate the colormap based solely on this information for the RGB
        functions along::

            d=  {   'blue':[0,0,0,0,1],
                    'green':[0,.35,.7,1,1],
                    'red':[1,1,1,1,1]}
            cmap = Colormap.get_cmap(d)

        """
        return self.cmap(
            {"blue": [0, 0, 0, 0, 1], "green": [0, 0.35, 0.7, 1, 1], "red": [1, 1, 1, 1, 1]}, reverse=False
        )

    def get_cmap_heat_r(self):
        """Return a heat colormap matplotlib-compatible colormap

        Same as :meth:`get_cmap_heat` but reversed
        """
        return self.cmap({"blue": [0, 0, 0, 0, 1], "green": [0, 0.35, 0.7, 1, 1], "red": [1, 1, 1, 1, 1]}, reverse=True)

    def get_cmap_rainbow(self):
        """colormap similar to rainbow colormap from R

        .. note:: The red is actually appearing on both sides... Yet
            this looks like what is coded in R 3.0.1

        """
        return self.cmap(
            {"blue": [0, 0, 0, 1, 1, 1, 0], "green": [0, 1, 1, 1, 0, 0, 0], "red": [1, 1, 0, 0, 0, 1, 1]}, reverse=False
        )

    def get_cmap_red_green(self):
        return self.cmap(
            {
                "green": [0, 0.4, 0.6, 0.75, 0.8, 0.9, 1, 0.9, 0.8, 0.6],
                "blue": [0, 0.4, 0.6, 0.75, 0.8, 0.7, 0.6, 0.35, 0.17, 0.1],
                "red": [1, 1, 1, 1, 1, 0.9, 0.8, 0.6, 0.3, 0.1],
            },
            reverse=True,
        )

    def test_colormap(self, cmap=None):
        """plot one colormap for testing

        By default, test the :meth:`get_cmap_heat`

        """
        if cmap is None:
            cmap = self.get_cmap_heat()
        import numpy as np
        from pylab import axis, clf, colorbar, linspace, pcolor, show

        A, B = np.meshgrid(linspace(0, 10, 100), linspace(0, 10, 100))
        clf()
        pcolor((A - 5) ** 2 + (B - 5) ** 2, cmap=cmap)
        colorbar()
        # show()
        axis("off")

    def plot_colormap(self, cmap_list=None):
        """cmap_list list of valid cmap or name of a set (sequential,
        diverging,)

        if none, plot all known colors

        .. .. plot::
        ..    :width:80%
        ..    :include-source:

        ..    from colormap import Colormap
        ..    c = Colormap()
        ..    c.plot_colormap('sequential')


        """
        from pylab import subplots

        if isinstance(cmap_list, str):
            if cmap_list in ["sequentials", "sequentials2", "qualitative", "misc", "diverging", "diverging_black"]:
                cmap_list = getattr(self, cmap_list)
            else:
                cmap_list = [cmap_list]
        if isinstance(cmap_list, list) is not True:
            raise TypeError(
                """input must be a list of srtings or a single string. Each string should be found. For a user-defined cmap, use test_colormap"""
            )
        for this in cmap_list:
            if this not in self.colormaps and this not in self.diverging_black:
                raise ValueError("unknown colormap name. Please check valid names in colormaps attribute")

        nrows = len(cmap_list)

        gradient = [x / 255 for x in range(0, 256)]
        gradient = [gradient, gradient]
        # np.vstack((gradient, gradient))

        fig, axes = subplots(nrows=nrows)
        fig.subplots_adjust(top=0.95, bottom=0.05, left=0.05, right=0.8)

        for ax, name in zip(axes, cmap_list):
            ax.imshow(gradient, aspect="auto", cmap=self.cmap(name))
            pos = list(ax.get_position().bounds)
            x_text = pos[2] + 0.08
            y_text = pos[1] + pos[3] / 2
            fig.text(x_text, y_text, name, va="center", ha="left", fontsize=10)

        # Turn off *all* ticks & spines, not just the ones with colormaps.
        for ax in axes:
            ax.set_axis_off()
