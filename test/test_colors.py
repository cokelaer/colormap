from colormap import colors
from colormap.colors import *
from easydev.easytest import assert_list_almost_equal


def test_hex2web():
    assert hex2web("#FFAA11") == "#FA1"

def test_web2hex():
    assert web2hex("#FA1") == "#FFAA11"

def test_rgb2yuv():
    assert_list_almost_equal(rgb2yuv(1,1,1) , (1,0,0))
    assert_list_almost_equal(rgb2yuv_int(255,255,255) , (255,0,0))

    assert_list_almost_equal(yuv2rgb(1,0,0) , (1,1,1))
    assert_list_almost_equal(yuv2rgb_int(255,0,0) , (255,255,255))


def test_rgb2hsv():
    assert_list_almost_equal( colors.rgb2hsv(0,1,1) , (0.5,1,1))
    assert_list_almost_equal(colors.rgb2hsv(0,255,255, normalised=False) , (0.5,1,1))

    assert_list_almost_equal(hsv2rgb(0.5,1,1) , (0,1,1))
    assert_list_almost_equal(colors.hsv2rgb(180,100,100, normalised=False), (0,1,1))

def test_rgb2hls():
    assert_list_almost_equal(colors.rgb2hls(0,1,1) , (0.5,0.5,1))
    assert_list_almost_equal(colors.rgb2hls(0,255,255,normalised=False) ,
            (0.5,0.5,1))

    assert_list_almost_equal(colors.hls2rgb(0.5,0.5,1), (0,1,1))
    assert_list_almost_equal(colors.hls2rgb(180, 50, 100, normalised=False),
            (0.,1,1))

def test_hex2dec():
    assert colors.hex2dec("FF") == 1

def test_rgb2hex():
    colors.rgb2hex(0,0,255)
    colors.rgb2hex(0,0,1)
    colors.rgb2hex(*(0,0,1))
    try:
        colors.rgb2hex([0,0])
        assert False
    except:
        assert True

    try:
        colors.rgb2hex(0,0,1000)
        assert False
    except:
        assert True

    try:
        colors.rgb2hex(0,0,-1000)
        assert False
    except:
        assert True

    try:
        colors.rgb2hex(0,0,10, normalised=True)
        assert False
    except:
        assert True


def testColors():
    # test constructors
    c = colors.Color("#FFF")
    c = colors.Color(rgb=(0,0,0))
    c = colors.Color(hls=(0,0,0))
    c = colors.Color(hsv=(0,0,0))
    c = colors.Color(c)
    try:
        colors.Color()
        assert False
    except:
        assert True
    try:
        colors.Color(object)
        assert False
    except:
        assert True

    
    # test setter/getter
    c = colors.Color("Blue")
    assert c.rgb == (0, 0 ,1)
    assert c.hex == "#0000FF"
    assert_list_almost_equal( c.hsv, (0.66666666666666,1,1))
    assert_list_almost_equal(c.hls, (0.666666666666666, .5,1))
    print(c)

    c.normalised = True
    c.name
    c.hsv
    c.hls
    print(c)
    assert c.rgb == (0,0,1)
    c.rgb = (0,0,1)
    c.hsv= (0,0,1)

    c.normalised = False

    # name can be changed and affects RGB/HEX
    c.name = "Magenta"
    assert c.rgb == colors._normalise(255, 0.0, 255)
    
    assert c.hex == "#FF00FF"

    # hex can be changed and affects name/HEX
    c.hex = "#F8F8FF"
    assert c.name == "Ghost White"   # non official name
    #assert c.rgb == 

    # RGB can be changed and affects name/HEX
    c.rgb = colors._normalise(248,248,255)
    assert c.name == "Ghost White"  # official name
    assert c.hex == "#F8F8FF"
    assert c.name == "Ghost White"  # non official but works
    assert c.hex == "#F8F8FF"
    c.saturation_hls = 0.5
    assert c.saturation_hls == 0.5

    c.lightness = 0.5
    assert c.lightness == 0.5
    c.hue = 0.5
    assert c.hue == 0.5

    c.hex = "#FF1F1F"
    assert c.name == "undefined"
    try:
        c.hex = "ZFF1F1F"
        assert False
    except:
        assert True

    c = colors.Color("red")
    assert c.red == 1
    assert c.green == 0
    assert c.blue == 0
    c.blue = 0.
    c.green=0.
    c.red = 0
    assert c.name == "Black"
    c.value
    c.value = 0.5
    c.yiq


def test_normalise():
    colors._normalise(255,255,255, mode='rgb') == (1,1,1)
    colors._normalise(*(255,255,255), mode='rgb') == (1,1,1)
    colors._normalise(*(360,100,100), mode='hls') == (1,1,1)
    colors._denormalise(*(1,1,1), mode='rgb') == (255,255,255)
    colors._denormalise(*(1,1,1), mode='hls') == (360,100,100)

def test_to_intensity():
    to_intensity(0.5)


def test_colormap():
    try:
        from pylab import close, clf, gcf
    except:
        return
    c = Colormap()
    cmap = c.get_cmap_heat()
    #c.test_cmap(cmap)
    f = gcf()
    #f.close()
    
    
    # design your own colormap
    d = {'blue': [0,0,0,1,1,1,0],
         'green':[0,1,1,1,0,0,0],
         'red':  [1,1,0,0,0,1,1]}
    cmap = c.cmap(d, reverse=True)
    cmap = c.get_cmap_rainbow()
    cmap = c.get_cmap_red_green()
    cmap = c.get_cmap_heat_r()


    t = ['#FF0000FF', '#FF4D00FF', '#FF9900FF', '#FFE500FF',
         '#CCFF00FF', '#80FF00FF', '#33FF00FF', '#00FF19FF',
         '#00FF66FF', '#00FFB2FF', '#00FFFFFF', '#00B3FFFF',
         '#0066FFFF', '#001AFFFF', '#3300FFFF', '#7F00FFFF',
         '#CC00FFFF','#FF00E6FF','#FF0099FF', '#FF004DFF']
    # FIXME: need to find a way to close the plot. close('all') does not work
    # c.plot_rgb_from_hex_list(t) 
    c.plot_colormap('misc')
    #c.plot_colormap('jet')
    c.test_colormap('jet')
    c.diverging
    c.colormaps
    c.sequentials
    c.sequentials2
    c.qualitative


    t = ['#FF0000FF', '#FF4D00FF', '#FF9900FF','#FFE500FF',
    '#CCFF00FF', '#80FF00FF','#33FF00FF', '#00FF19FF',
    '#00FF66FF','#00FFB2FF','#00FFFFFF','#00B3FFFF',
    '#0066FFFF','#001AFFFF','#3300FFFF','#7F00FFFF',
    '#CC00FFFF','#FF00E6FF','#FF0099FF','#FF004DFF']
    c.plot_rgb_from_hex_list(t)
    c.test_colormap() # no input plots the heat map


def test_HEX():

    h = HEX()
    h.get_standard_hex_color("0xFFF")
    try:
        h.get_standard_hex_color(22)
        assert False
    except:
        assert True

    try:
        h.get_standard_hex_color("r")
        assert False
    except:
        assert True


    try:
        h.get_standard_hex_color("rrrrrrrrrrrr")
        assert False
    except:
        assert True

    try:
        h.get_standard_hex_color("#AAAZZZ")
        assert False
    except:
        assert True

    try:
        h.get_standard_hex_color("#AAAA")
        assert False
    except:
        assert True


