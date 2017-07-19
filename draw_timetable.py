import sys

import seaborn as sns
import numpy
import pandas
import datetime


def colorstr(rgb): return "#%02x%02x%02x" % (rgb[0],rgb[1],rgb[2])


def hsl_to_rgb(h, s, l):
    c = (1 - abs(2*l - 1)) * s
    x = c * (1 - abs(h *1.0 / 60 % 2 - 1))
    m = l - c/2
    if h < 60:
        r, g, b = c + m, x + m, 0 + m
    elif h < 120:
        r, g, b = x + m, c+ m, 0 + m
    elif h < 180:
        r, g, b = 0 + m, c + m, x + m
    elif h < 240:
        r, g, b, = 0 + m, x + m, c + m
    elif h < 300:
        r, g, b, = x + m, 0 + m, c + m
    else:
        r, g, b, = c + m, 0 + m, x + m
    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)
    return (r,g,b)

class scalableVectorGraphics:

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.out = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   height="%d"
   width="%d"
   id="svg2"
   version="1.1"
   inkscape:version="0.48.4 r9939"
   sodipodi:docname="easyfig">
  <metadata
     id="metadata122">
    <rdf:RDF>
      <cc:Work
         rdf:about="">
        <dc:format>image/svg+xml</dc:format>
        <dc:type
           rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
        <dc:title>Easyfig</dc:title>
      </cc:Work>
    </rdf:RDF>
  </metadata>
  <defs
     id="defs120" />
  <sodipodi:namedview
     pagecolor="#ffffff"
     bordercolor="#666666"
     borderopacity="1"
     objecttolerance="10"
     gridtolerance="10"
     guidetolerance="10"
     inkscape:pageopacity="0"
     inkscape:pageshadow="2"
     inkscape:window-width="640"
     inkscape:window-height="480"
     id="namedview118"
     showgrid="false"
     inkscape:zoom="0.0584"
     inkscape:cx="2500"
     inkscape:cy="75.5"
     inkscape:window-x="55"
     inkscape:window-y="34"
     inkscape:window-maximized="0"
     inkscape:current-layer="svg2" />
  <title
     id="title4">Easyfig</title>
  <g
     style="fill-opacity:1.0; stroke:black; stroke-width:1;"
     id="g6">''' % (self.height, self.width)

    def drawLine(self, x1, y1, x2, y2, th=1, cl=(0, 0, 0), alpha = 1.0):
        self.out += '  <line x1="%d" y1="%d" x2="%d" y2="%d"\n        stroke-width="%d" stroke="%s" stroke-opacity="%f" stroke-linecap="butt" />\n' % (x1, y1, x2, y2, th, colorstr(cl), alpha)

    def drawPath(self, xcoords, ycoords, th=1, cl=(0, 0, 0), alpha=0.9):
        self.out += '  <path d="M%d %d' % (xcoords[0], ycoords[0])
        for i in range(1, len(xcoords)):
            self.out += ' L%d %d' % (xcoords[i], ycoords[i])
        self.out += '"\n        stroke-width="%d" stroke="%s" stroke-opacity="%f" stroke-linecap="butt" fill="none" z="-1" />\n' % (th, colorstr(cl), alpha)


    def writesvg(self, filename):
        outfile = open(filename, 'w')
        outfile.write(self.out + ' </g>\n</svg>')
        outfile.close()

    def drawRightArrow(self, x, y, wid, ht, fc, oc=(0,0,0), lt=1):
        if lt > ht /2:
            lt = ht/2
        x1 = x + wid
        y1 = y + ht/2
        x2 = x + wid - ht / 2
        ht -= 1
        if wid > ht/2:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fc), colorstr(oc), lt)
            self.out += '           points="%d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d" />\n' % (x, y+ht/4, x2, y+ht/4,
                                                                                                x2, y, x1, y1, x2, y+ht,
                                                                                                x2, y+3*ht/4, x, y+3*ht/4)
        else:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fc), colorstr(oc), lt)
            self.out += '           points="%d,%d %d,%d %d,%d" />\n' % (x, y, x, y+ht, x + wid, y1)

    def drawLeftArrow(self, x, y, wid, ht, fc, oc=(0,0,0), lt=1):
        if lt > ht /2:
            lt = ht/2
        x1 = x + wid
        y1 = y + ht/2
        x2 = x + ht / 2
        ht -= 1
        if wid > ht/2:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fc), colorstr(oc), lt)
            self.out += '           points="%d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d" />\n' % (x1, y+ht/4, x2, y+ht/4,
                                                                                                x2, y, x, y1, x2, y+ht,
                                                                                                x2, y+3*ht/4, x1, y+3*ht/4)
        else:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fc), colorstr(oc), lt)
            self.out += '           points="%d,%d %d,%d %d,%d" />\n' % (x, y1, x1, y+ht, x1, y)

    def drawBlastHit(self, x1, y1, x2, y2, x3, y3, x4, y4, fill=(0, 0, 255), lt=2, alpha=0.1):
        self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d" fill-opacity="%f"\n' % (colorstr(fill), colorstr((0,0,0)), lt, alpha)
        self.out += '           points="%d,%d %d,%d %d,%d %d,%d" />\n' % (x1, y1, x2, y2, x3, y3, x4, y4)

    def drawGradient(self, x1, y1, wid, hei, minc, maxc):
        self.out += '  <defs>\n    <linearGradient id="MyGradient" x1="0%" y1="0%" x2="0%" y2="100%">\n'
        self.out += '      <stop offset="0%%" stop-color="%s" />\n' % colorstr(maxc)
        self.out += '      <stop offset="100%%" stop-color="%s" />\n' % colorstr(minc)
        self.out += '    </linearGradient>\n  </defs>\n'
        self.out += '  <rect fill="url(#MyGradient)" stroke-width="0"\n'
        self.out += '        x="%d" y="%d" width="%d" height="%d"/>\n' % (x1, y1, wid, hei)

    def drawGradient2(self, x1, y1, wid, hei, minc, maxc):
        self.out += '  <defs>\n    <linearGradient id="MyGradient2" x1="0%" y1="0%" x2="0%" y2="100%">\n'
        self.out += '      <stop offset="0%%" stop-color="%s" />\n' % colorstr(maxc)
        self.out += '      <stop offset="100%%" stop-color="%s" />\n' % colorstr(minc)
        self.out += '    </linearGradient>\n</defs>\n'
        self.out += '  <rect fill="url(#MyGradient2)" stroke-width="0"\n'
        self.out += '        x="%d" y="%d" width="%d" height="%d" />\n' % (x1, y1, wid, hei)

    def drawOutRect(self, x1, y1, wid, hei, fill=(255, 255, 255), outfill=(0, 0, 0), lt=1, alpha=1.0, alpha2=1.0):
        self.out += '  <rect stroke="%s" stroke-width="%d" stroke-opacity="%f"\n' % (colorstr(outfill), lt, alpha)
        self.out += '        fill="%s" fill-opacity="%f"\n' % (colorstr(fill), alpha2)
        self.out += '        x="%d" y="%d" width="%d" height="%d" />\n' % (x1, y1, wid, hei)

    def drawAlignment(self, x, y, fill, outfill, lt=1, alpha=1.0, alpha2=1.0):
        self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d" stroke-opacity="%f" fill-opacity="%f"\n' % (colorstr(fill), outfill, lt, alpha, alpha2)
        self.out += '  points="'
        for i, j in zip(x, y):
            self.out += str(i) + ',' + str(j) + ' '
        self.out += '" />\n'
             # print self.out.split('\n')[-2]



    def drawSymbol(self, x, y, size, fill, symbol, alpha=1.0, lt=1):
        x0 = x - size/2
        x1 = size/8 + x - size/2
        x2 = size/4 + x - size/2
        x3 = size*3/8 + x - size/2
        x4 = size/2 + x - size/2
        x5 = size*5/8 + x - size/2
        x6 = size*3/4 + x - size/2
        x7 = size*7/8 + x - size/2
        x8 = size + x - size/2
        y0 = y - size/2
        y1 = size/8 + y - size/2
        y2 = size/4 + y - size/2
        y3 = size*3/8 + y - size/2
        y4 = size/2 + y - size/2
        y5 = size*5/8 + y - size/2
        y6 = size*3/4 + y - size/2
        y7 = size*7/8 + y - size/2
        y8 = size + y - size/2
        if symbol == 'o':
            self.out += '  <circle stroke="%s" stroke-width="%d" stroke-opacity="%f"\n' % (colorstr((0, 0, 0)), lt, alpha)
            self.out += '        fill="%s" fill-opacity="%f"\n' % (colorstr(fill), alpha)
            self.out += '        cx="%d" cy="%d" r="%d" />\n' % (x, y, size/2)
        elif symbol == 'x':
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d" stroke-opacity="%f" fill-opacity="%f"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt, alpha, alpha)
            self.out += '           points="%d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d" />\n' % (x0, y2, x2, y0, x4, y2, x6, y0, x8, y2,
                                                                                                                             x6, y4, x8, y6, x6, y8, x4, y6, x2, y8,
                                                                                                                             x0, y6, x2, y4)
        elif symbol == '+':
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d" stroke-opacity="%f" fill-opacity="%f"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt, alpha, alpha)
            self.out += '           points="%d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d" />\n' % (x2, y0, x6, y0, x6, y2, x8, y2, x8, y6,
                                                                                                                             x6, y6, x6, y8, x2, y8, x2, y6, x0, y6,
                                                                                                                             x0, y2, x2, y2)
        elif symbol == 's':
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d" stroke-opacity="%f" fill-opacity="%f"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt, alpha, alpha)
            self.out += '           points="%d,%d %d,%d %d,%d %d,%d" />\n' % (x0, y0, x0, y8, x8, y8, x8, y0)
        elif symbol == '^':
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d" stroke-opacity="%f" fill-opacity="%f"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt, alpha, alpha)
            self.out += '           points="%d,%d %d,%d %d,%d %d,%d %d,%d %d,%d" />\n' % (x0, y0, x2, y0, x4, y4, x6, y0, x8, y0, x4, y8)
        elif symbol == 'v':
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d" stroke-opacity="%f" fill-opacity="%f"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt, alpha, alpha)
            self.out += '           points="%d,%d %d,%d %d,%d %d,%d %d,%d %d,%d" />\n' % (x0, y8, x2, y8, x4, y4, x6, y8, x8, y8, x4, y0)
        elif symbol == 'u':
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d" stroke-opacity="%f" fill-opacity="%f"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt, alpha, alpha)
            self.out += '           points="%d,%d %d,%d %d,%d" />\n' % (x0, y8, x4, y0, x8, y8)
        elif symbol == 'd':
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d" stroke-opacity="%f" fill-opacity="%f"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt, alpha, alpha)
            self.out += '           points="%d,%d %d,%d %d,%d" />\n' % (x0, y0, x4, y8, x8, y0)
        else:
            sys.stderr.write(symbol + '\n')
            sys.stderr.write('Symbol not found, this should not happen.. exiting')
            sys.exit()








    def drawRightFrame(self, x, y, wid, ht, lt, frame, fill):
        if lt > ht /2:
            lt = ht /2
        if frame == 1:
            y1 = y + ht/2
            y2 = y + ht * 3/8
            y3 = y + ht * 1/4
        elif frame == 2:
            y1 = y + ht * 3/8
            y2 = y + ht * 1/4
            y3 = y + ht * 1/8
        elif frame == 0:
            y1 = y + ht * 1/4
            y2 = y + ht * 1/8
            y3 = y + 1
        x1 = x
        x2 = x + wid - ht/8
        x3 = x + wid
        if wid > ht/8:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt)
            self.out += '           points="%d,%d %d,%d %d,%d %d,%d %d,%d" />\n' % (x1, y1, x2, y1, x3, y2, x2, y3, x1, y3)
        else:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt)
            self.out += '           points="%d,%d %d,%d %d,%d" />\n' % (x1, y1, x3, y2, x1, y3)

    def drawRightFrameRect(self, x, y, wid, ht, lt, frame, fill):
        if lt > ht /2:
            lt = ht /2
        if frame == 1:
            y1 = y + ht / 4
        elif frame == 2:
            y1 = y + ht /8
        elif frame == 0:
            y1 = y + 1
        hei = ht /4
        x1 = x
        self.out += '  <rect fill="%s" stroke-width="%d"\n' % (colorstr(fill), lt)
        self.out += '        x="%d" y="%d" width="%d" height="%d" />\n' % (x1, y1, wid, hei)

    def drawLeftFrame(self, x, y, wid, ht, lt, frame, fill):
        if lt > ht /2:
            lt = ht /2
        if frame == 1:
            y1 = y + ht
            y2 = y + ht * 7/8
            y3 = y + ht * 3/4
        elif frame == 2:
            y1 = y + ht * 7/8
            y2 = y + ht * 3/4
            y3 = y + ht * 5/8
        elif frame == 0:
            y1 = y + ht * 3/4
            y2 = y + ht * 5/8
            y3 = y + ht / 2
        x1 = x + wid
        x2 = x + ht/8
        x3 = x
        if wid > ht/8:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt)
            self.out += '           points="%d,%d %d,%d %d,%d %d,%d %d,%d" />\n' % (x1, y1, x2, y1, x3, y2, x2, y3, x1, y3)
        else:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt)
            self.out += '           points="%d,%d %d,%d %d,%d" />\n' % (x1, y1, x3, y2, x1, y3)

    def create_pattern(self, id, fill, pattern, width, line_width):
        fill = colorstr(fill)
        if pattern == 'horizontal':
            self.out += '    <defs>\n'
            self.out += '      <pattern id="%s" width="%d" height="%d" patternUnits="userSpaceOnUse">\n' % (id, width, width)
            self.out += '        <line x1="0" y1="0" x2="%d" y2="0" style="stroke:%s; stroke-width:%d; fill:#FFFFFF" />\n' % (width, fill, line_width)
            self.out += '      </pattern>\n'
            self.out += '   </defs>\n'
        elif pattern == 'forward_diag':
            self.out += '    <defs>\n'
            self.out += '      <pattern id="%s" width="%d" height="%d" patternTransform="rotate(45 0 0)" patternUnits="userSpaceOnUse">\n' % (id, width, width)
            self.out += '        <line x1="0" y1="0" x2="0" y2="%d" style="stroke:%s; stroke-width:%d; fill:#FFFFFF" />\n' % (width, fill, line_width)
            self.out += '      </pattern>\n'
            self.out += '   </defs>\n'
        elif pattern == 'reverse_diag':
            self.out += '    <defs>\n'
            self.out += '      <pattern id="%s" width="%d" height="%d" patternTransform="rotate(135 0 0)" patternUnits="userSpaceOnUse">\n' % (id, width, width)
            self.out += '        <line x1="0" y1="0" x2="0" y2="%d" style="stroke:%s; stroke-width:%d; fill:#FFFFFF" />\n' % (width, fill, line_width)
            self.out += '      </pattern>\n'
            self.out += '   </defs>\n'

    def drawPatternRect(self, x, y, width, height, id, fill, lt):
        fill = colorstr(fill)
        self.out += '  <rect style="fill:#FFFFFF; stroke: %s; stroke-width: %d; stroke-alignment: inner;"\n' % (fill, lt)
        self.out += '        x="%d" y="%d" width="%d" height="%d" />\n' % (x, y, width, height)
        self.out += '  <rect style="fill:url(#%s); stroke: %s; stroke-width: %d; stroke-alignment: inner;"\n' % (id, fill, lt)
        self.out += '        x="%d" y="%d" width="%d" height="%d" />\n' % (x, y, width, height)


    def drawLeftFrameRect(self, x, y, wid, ht, lt, frame, fill):
        if lt > ht /2:
            lt = ht /2
        if frame == 1:
            y1 = y + ht * 3/4
        elif frame == 2:
            y1 = y + ht * 5/8
        elif frame == 0:
            y1 = y + ht / 2
        hei = ht /4
        x1 = x
        self.out += '  <rect fill="%s" stroke-width="%d"\n' % (colorstr(fill), lt)
        self.out += '        x="%d" y="%d" width="%d" height="%d" />\n' % (x1, y1, wid, hei)

    def drawPointer(self, x, y, ht, lt, fill):
        x1 = x - int(round(0.577350269 * ht/2))
        x2 = x + int(round(0.577350269 * ht/2))
        y1 = y + ht/2
        y2 = y + 1
        self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt)
        self.out += '           points="%d,%d %d,%d %d,%d" />\n' % (x1, y2, x2, y2, x, y1)

    def drawDash(self, x1, y1, x2, y2, exont, dashPattern, color=(0,0,0)):
        self.out += '  <line x1="%d" y1="%d" x2="%d" y2="%d"\n' % (x1, y1, x2, y2)
        self.out += '       style="stroke-dasharray: %d, %d, %d, %d"\n' % dashPattern
        self.out += '       stroke="%s" stroke-width="%d" />\n' % (colorstr(color), exont)


    def drawPolygon(self, x_coords, y_coords, colour=(0,0,255)):
        self.out += '  <polygon points="'
        for i,j in zip(x_coords, y_coords):
            self.out += str(i) + ',' + str(j) + ' '
        self.out += '"\nstyle="fill:%s;stroke=none" />\n'  % colorstr(colour)
    def writeString(self, thestring, x, y, size, ital=False, bold=False, rotate=0, justify='left'):
        if rotate != 0:
            x, y = y, x
        self.out += '  <text\n'
        self.out += '    style="font-size:%dpx;font-style:normal;font-weight:normal;z-index:10\
;line-height:125%%;letter-spacing:0px;word-spacing:0px;fill:#111111;fill-opacity:1;stroke:none;font-family:Sans"\n' % size
        if justify == 'right':
            self.out += '    text-anchor="end"\n'
        elif justify == 'middle':
            self.out += '    text-anchor="middle"\n'
        if rotate == 1:
            self.out += '    x="-%d"\n' % x
        else:
            self.out += '    x="%d"\n' % x
        if rotate == -1:
            self.out += '    y="-%d"\n' % y
        else:
            self.out += '    y="%d"\n' % y
        self.out += '    sodipodi:linespacing="125%"'
        if rotate == -1:
            self.out += '\n    transform="matrix(0,1,-1,0,0,0)"'
        if rotate == 1:
            self.out += '\n    transform="matrix(0,-1,1,0,0,0)"'
        self.out += '><tspan\n      sodipodi:role="line"\n'
        if rotate == 1:
            self.out += '      x="-%d"\n' % x
        else:
            self.out += '      x="%d"\n' % x
        if rotate == -1:
            self.out += '      y="-%d"' % y
        else:
            self.out += '      y="%d"' % y
        if ital and bold:
            self.out += '\nstyle="font-style:italic;font-weight:bold"'
        elif ital:
            self.out += '\nstyle="font-style:italic"'
        elif bold:
            self.out += '\nstyle="font-style:normal;font-weight:bold"'
        self.out += '>' + thestring + '</tspan></text>\n'





class patient:
    def __init__(self, mrn, name, erap):
        self.mrn = mrn
        self.name = name
        self.extract_ids = []
        self.antibiotics = []
        self.stays = []
        self.events = []
        self.erap = erap

    def add_extract(self, extract, time, status):
        self.extract_ids.append((extract, time, status))

    def add_stay(self, start, end, loc):
        self.stays.append((start, end, loc))

    def add_event(self, time, what, loc):
        self.events.append((time, what, loc))

    def add_antibiotics(self, time, what):
        self.antibiotics.append((time, what))



def get_time(astring):
    if astring == '':
        return None
    elif ' ' in astring:
        date, time = astring.split()
        if ':' in time:
            hour, minute, second = time.split(':')
        else:
            hour, minute = time[:2], time[2:]
            second = 0
    else:
        date = astring
        hour, minute, second = 12, 0, 0
    if '-' in date:
        year, month, day = date.split('-')
    else:
        month, day, year = date.split('/')
        if len(year) == 2:
            year = '20' + year
    month, day, year, hour, minute, second = map(int, [month, day, year, hour, minute, second])
    return datetime.datetime(year, month, day, hour, minute, second)



def load_patients(pat_file):
    out_dict = {'timeline':{}}
    patient_order = []
    with open(pat_file) as f:
        for line in f:
            if not line.startswith('#'):
                extract, date, erap, mrn, name, status = line.rstrip().split('\t')[:6]
                time = get_time(date)
                if mrn in out_dict:
                    out_dict[mrn].add_extract(extract, time, status)
                else:
                    if mrn == 'n/a':
                        num = int(line.rstrip().split('\t')[6])
                        if not date in out_dict['timeline']:
                            out_dict['timeline'][date] = []
                        if extract != 'Environmental':
                            out_dict['timeline'][date].append((extract, name, status))
                            num -= 1
                        for q in range(num):
                            out_dict['timeline'][date].append(('Environmental', name, 'Culture negative'))
                    else:
                        aninstance = patient(mrn, name, erap)
                        aninstance.add_extract(extract, time, status)
                        out_dict[mrn] = aninstance
                        patient_order.append(mrn)
    return out_dict, patient_order


def get_events(pat_dict, event_file):
    first_encounter = None
    last_encounter = None
    hosp_enc_loc = set()
    other_locs = set()
    with open(event_file) as f:
        f.readline()
        for line in f:
            if len(line.rstrip().split('\t')) >= 10:
                mrn, enc_date, department, enc_type, age, sex, bmi, smoker, admit, discharge = line.rstrip().split('\t')[:10]
            elif len(line.rstrip().split('\t')) == 9:
                mrn, enc_date, department, enc_type, age, sex, bmi, smoker, admit = line.rstrip().split('\t')[:9]
            elif len(line.rstrip().split('\t')) == 8:
                mrn, enc_date, department, enc_type, age, sex, bmi, smoker = line.rstrip().split('\t')[:8]
                discharge = None
            elif len(line.rstrip().split('\t')) < 8:
                mrn, enc_date, department, enc_type, = line.rstrip().split('\t')[:4]
                sex = None
                bmi = None
                smoker = None
                admit = None
            else:
                print line.rstrip(), 'error'
            if mrn in pat_dict:
                enc_date = get_time(enc_date)
                if first_encounter is None or enc_date < first_encounter:
                    first_encounter = enc_date
                if last_encounter is None or enc_date > last_encounter:
                    last_encounter = enc_date
                if enc_type == 'Hospital Encounter':
                    hosp_enc_loc.add(department)
                    admit = get_time(admit)
                    if admit < first_encounter:
                        first_encounter = admit
                    discharge = get_time(discharge)
                    if discharge is None:
                        discharge = admit + datetime.timedelta(hours=12)
                        sys.stderr.write('No discharge time:\n' + line.rstrip() + '\n')
                    pat_dict[mrn].add_stay(admit, discharge, department)
                else:
                    other_locs.add(department)
                    pat_dict[mrn].add_event(enc_date, enc_type, department)
    return hosp_enc_loc, other_locs, (first_encounter, last_encounter)

def add_fine_loc(pat_dict, event_file):
    new_locs = set()
    with open(event_file) as f:
        f.readline()
        for line in f:
            splitline = line.split('\t')
            splitline = filter(lambda x: not x in ['', '\n'], splitline)
            patient = splitline[1]
            for i in pat_dict:
                try:
                    if pat_dict[i].erap == patient:
                        pat_dict_index = i
                except:
                    pass
            pat_dict[pat_dict_index].stays = []
            for i in range(2, len(splitline), 3):
                loc, start, stop = splitline[i:i+3]
                t_start = get_time(start)
                t_stop = get_time(stop)
                if loc != 'unknown':
                    new_locs.add(loc)
                    pat_dict[pat_dict_index].add_stay(t_start, t_stop, loc)
    return new_locs


def get_antibiotics(pat_dict, antibiotics_file):
    with open(antibiotics_file) as f:
        f.readline()
        for line in f:
            mrn, enc_date, department, enc_type, med_id, med_name = line.split('\t')[:6]
            if mrn in pat_dict:
                enc_date = get_time(enc_date)
                pat_dict[mrn].add_antibiotics(enc_date, med_name)

def get_x_time(time, start_time, end_time, width):
    totalsecs = (end_time-start_time).total_seconds()
    time_to_event = (time-start_time).total_seconds()
    return time_to_event / totalsecs * width

def get_snp_profile(filename):
    max_no = 5
    max_length = 1000
    lastchrom = None
    with open(filename) as snv:
        pos_list = []
        base_list = []
        for line in snv:
            if line.startswith('##'):
                pass
            elif line.startswith('#CHROM'):
                refs = line.split()[9:]
            else:
                chrom, pos, ID, ref, alt, qual, filter, info, format = line.split()[:9]
                base_no = map(int, line.split()[9:])
                bases = alt.split(',')
                if lastchrom == None:
                    lastchrom = chrom
                if chrom == lastchrom:
                    pos_list.append(int(pos))
                    alist = []
                    for i in base_no:
                        alist.append(bases[i-1])
                    base_list.append(alist)
    curr_list = pos_list[:max_no-1]
    filter_pos = set()
    # for num, i in enumerate(pos_list[max_no-1:]):
    #     curr_list.append(i)
    #     if curr_list[-1] - curr_list[0] <= max_length:
    #         for j in curr_list:
    #             filter_pos.add(j)
    #     curr_list = curr_list[1:]
    out_pos_list = []
    base_dict = {}
    new_refs = []
    for i in refs:
        new_refs.append(i.split('.')[0])
        base_dict[i.split('.')[0]] = ''
    refs = new_refs
    for i, j in zip(pos_list, base_list):
        if not i in filter_pos:
            out_pos_list.append(i)
            for num, k in enumerate(j):
                base_dict[refs[num]] += k
    return out_pos_list, base_dict








def draw_timeline(pat_dict, orderlist, outfile, hosp_enc_loc, other_loc, snv_file, vent_data, encounter_span):
    symbols = 'ox+sud^v'
    loc_color = {}
    color_len = len(hosp_enc_loc | other_loc)
    s_list = [0.3, 0.6, 0.7]
    l_list = [0.6, 0.8]
    other_loc = other_loc - hosp_enc_loc
    hosp_enc_loc = list(hosp_enc_loc)
    other_loc2 = list(other_loc)
    other_loc = list(other_loc)
    extract_color = {'outbreak_a':(120,17,174), 'outbreak_b':(82,222,228), 'outbreak_c':(102,239,85), 'outbreak_a_bac':(120,17,174), 'missing_bac':(200, 200, 200), 'missing':(200, 200, 200),
                     'outbreak_b_bac':(82,222,228), 'outbreak_c_bac':(102,239,85), 'precursor':(250,150,50), 'unrelated':(0,102,255), 'unrelated_bac':(0,102,255), 'Culture negative':(255,255,255), 'Event':(255,0,0)}
    event_types = set()
    antibiotic_types = set()
    snv_pos_list, snv_base_dict = get_snp_profile(snv_file)
    for i in orderlist:
        for j in pat_dict[i].antibiotics:
            antibiotic_types.add(j[1])
        for j in pat_dict[i].events:
            event_types.add(j[1])
    locations = []
    for i in hosp_enc_loc:
        locations.append(i)
        try:
            x = other_loc.pop()
            locations.append(x)
            x = other_loc.pop()
            locations.append(x)
        except IndexError:
            pass
    # for num, i in enumerate(hosp_enc_loc):
    #     h = num * 360 / color_len
    #     s = s_list[num%3]
    #     l = l_list[num%2]
    #     color = hsl_to_rgb(h, s, l)
        # loc_color[i] = color
    loc_color = {"314":(172,156,61),
"316":(140, 115, 191),
"317":(140, 115, 191),
"318":(100, 180, 120),
"319":(100, 180, 120),
"320":(190, 91, 135),
"321":(190, 91, 135),
"322":(193, 86, 62),
"323":(193, 86, 62),

"C5M":(205,71,97),
"KP6":(69,192,151),
"MICU":(164,61,143),
"MPCU":(143,176,61),
"N08C":(106,112,215),
"N08W":(205,156,46),
"N09C":(85,54,135),
"N09E":(90,165,84),
"N09W":(192,127,213),
"N10C":(186,154,64),
"N10W":(98,142,214),
"N11E":(199,109,57),
"N11W":(214,123,182),
"NICU":(151,140,67),
"OR":(204,73,131),
"PICU":(152,46,36),
"P05":(155,61,93),
"P04":(210,110,93),
}


    ab_color = {}
    for num, i in enumerate(antibiotic_types):
        h = num * 360 / color_len
        s = s_list[num%3]
        l = l_list[num%2]
        color = hsl_to_rgb(h, s, l)
        ab_color[i] = color
    event_dict = {}
    for num, i in enumerate(event_types):
        event_dict[i] = symbols[num % len(symbols)]
    left_buffer = 500
    top_buffer = 1000
    right_buffer = 1000
    bottom_buffer = 100
    width = 5000
    height = 10000
    svg = scalableVectorGraphics(height, width + left_buffer + right_buffer)
    pat_height = 80
    stay_height = 20
    font_size = 36
    start_dt, end_dt = encounter_span
    first_tick = start_dt - datetime.timedelta(hours=start_dt.hour, minutes=start_dt.minute, seconds=start_dt.second)
    first_tick += datetime.timedelta(hours=24)
    extract_list = []
    for num, i in enumerate(orderlist):
        if num % 2 == 0:
            svg.drawOutRect(left_buffer, num * pat_height + top_buffer, width, pat_height, fill=(220, 220, 220), lt=0)
    count = 0
    firstday = datetime.datetime(2014, 9, 1)
    while first_tick < end_dt:
        count += 1
        x = get_x_time(first_tick, start_dt, end_dt, width)
        if count % 5 == 0:
            the_delta = first_tick - firstday
            svg.drawLine(left_buffer + x, top_buffer, left_buffer + x, len(orderlist) * pat_height + top_buffer, th=3)
            svg.writeString('Day ' + str(the_delta.days), left_buffer + x, top_buffer - 10, font_size, rotate=-1,justify='right')
            svg.writeString(first_tick.isoformat()[:10], left_buffer + x, top_buffer - 10, font_size, rotate=-1,justify='right')
        else:
            svg.drawLine(left_buffer + x, top_buffer, left_buffer + x, len(orderlist) * pat_height + top_buffer, th=2)
        first_tick += datetime.timedelta(hours=24*7)
    strain_to_name_dict = {}
    extract_to_pat_and_time = {}
    pattern_dict = {}
    y_axis_dict = {}
    for num, i in enumerate(orderlist):
        print pat_dict[i].erap
        print pat_dict[i].name
        y_axis_dict[pat_dict[i].erap] = num * pat_height + pat_height/2 + top_buffer
        svg.writeString(pat_dict[i].erap, left_buffer - 5, num * pat_height + pat_height/2 + font_size/3 + top_buffer, font_size, justify='right')
        svg.writeString(pat_dict[i].name, left_buffer + width + 5, num * pat_height + pat_height/2 + font_size/3 + top_buffer, font_size)
        for j in pat_dict[i].stays:
            start, end, loc = j
            startx = get_x_time(start, start_dt, end_dt, width)
            endx = get_x_time(end, start_dt, end_dt, width)
            color = loc_color[loc]
            if start_dt <= start <= end <= end_dt:
                if loc.isdigit():
                    svg.drawOutRect(startx + left_buffer, num * pat_height + top_buffer + (pat_height - stay_height) / 2, endx - startx, stay_height, fill=color, lt=0)
                else:
                    if loc in pattern_dict:
                        pattern = pattern_dict[loc]
                    else:
                        svg.create_pattern(loc, color, 'forward_diag', 30, 40)
                    svg.drawPatternRect(startx + left_buffer, num * pat_height + top_buffer + (pat_height - stay_height) / 2, endx - startx, stay_height, loc, fill=color, lt=2)
        # for j in pat_dict[i].antibiotics:
        #     time, antibiotic = j
        #     x = get_x_time(time, start_dt, end_dt, width)
        #     color = ab_color[antibiotic]
        #     if start_dt <= time <= end_dt:
        #         svg.drawSymbol(x + left_buffer, top_buffer + num * pat_height + pat_height/2 + stay_height/2 + 7, 10, color, 's', lt=0)
        # for j in pat_dict[i].events:
        #     time, what, loc = j
        #     x = get_x_time(time, start_dt, end_dt, width)
        #     color = loc_color[loc]
        #     symbol = event_dict[what]
        #     if start_dt <= time <= end_dt:
        #         svg.drawSymbol(x + left_buffer, top_buffer + num * pat_height + 10, 10, color, symbol, lt=0)
        for j in pat_dict[i].extract_ids:
            id, time, status = j
            extract_to_pat_and_time[id] = (i, time)
            strain_to_name_dict[id] = pat_dict[i].name
            if (status[:8] == 'outbreak' or status == 'precursor') and '.' in id:
                extract_list.append((time, id))
            x = get_x_time(time, start_dt, end_dt, width)
            color = extract_color[status]
            if start_dt <= time <= end_dt:
                if '.' in id and (status.endswith('bac') or status == 'precursor'):
                    svg.drawSymbol(x + left_buffer, top_buffer +  num * pat_height + pat_height/2, stay_height*2, color, 'o')
                elif id == 'Surveillance' or '.' in id:
                    svg.drawSymbol(x + left_buffer, top_buffer +  num * pat_height + pat_height/2, stay_height*2, color, 's')
                elif status.endswith('bac'):
                    svg.drawSymbol(x + left_buffer, top_buffer +  num * pat_height + pat_height/2, stay_height*2, color, 'o', lt=2)
                    svg.drawSymbol(x + left_buffer, top_buffer +  num * pat_height + pat_height/2, stay_height*2, color, 'x', lt=2)
                else:
                    svg.drawSymbol(x + left_buffer, top_buffer +  num * pat_height + pat_height/2, stay_height*2, color, 's', lt=2)
                    svg.drawSymbol(x + left_buffer, top_buffer +  num * pat_height + pat_height/2, stay_height*2, color, 'x', lt=2)
    lastx = -10000000000
    overlap = [set()]
    svg.writeString('timeline', left_buffer - 5, top_buffer + num * pat_height + pat_height/2 + pat_height + font_size/3, font_size, justify='right')
    svg.drawLine(left_buffer, top_buffer + num * pat_height + pat_height/2 + pat_height, left_buffer + width, top_buffer + num * pat_height + pat_height/2 + pat_height, 10)
    timeline_height = 15
    for i in pat_dict['timeline']:
        mod = 0
        for j in pat_dict['timeline'][i]:
            extract, name, status = j
            time = get_time(i)
            strain_to_name_dict[extract] = name
            # print extract, status
            if (status[:8] == 'outbreak' or status == 'precursor') and '.' in extract:
                extract_list.append((time, extract))
            x = get_x_time(time, start_dt, end_dt, width)
            color = extract_color[status]
            if start_dt <= time <= end_dt:
                if name == 'Environmental':
                    symbol = 'u'
                elif name == 'Staff culture':
                    symbol = 's'
                svg.drawSymbol(x + left_buffer, top_buffer + num * pat_height + pat_height/2 + pat_height + timeline_height*mod, timeline_height, color, symbol)
                mod += 1
    base_col = {'A':( 51, 102, 153), 'T':(242, 239, 119), 'G':(0,128,0), 'C':(150,0,24)}
    extract_list.sort()
    colcount = 0
    for i in extract_list:
        time, id = i
        for j in snv_base_dict:
            if id.split('.')[0] in j:
                colcount += 1
                rowcount = len(snv_base_dict[j])
    the_array = numpy.zeros((colcount, rowcount))
    for numa, i in enumerate(extract_list):
        time, id = i
        for j in snv_base_dict:
            if id.split('.')[0] in j:
                bases = snv_base_dict[j]
        for numb, j in enumerate(bases):
            if j == 'A':
                basenumber = 0
            if j == 'T':
                basenumber = 1
            if j == 'G':
                basenumber = 2
            if j == 'C':
                basenumber = 3
            the_array[numa][numb] = basenumber
    df = pandas.DataFrame(the_array)
    cluster = sns.clustermap(df, col_cluster=False, row_cluster=True)
    ordered_extract_list = []
    for i in cluster.dendrogram_row.reordered_ind:
        ordered_extract_list.append(extract_list[i])

    ordered_extract_list_new = []
    for i in ['ER02837', 'ER02637', 'ER03556', 'ER04324', 'ER03930', 'ER04397', 'ER03759', 'ER04440', 'ER04407', 'ER03717', 'ER04119', 'ER03760',\
              'ER04115', 'ER03763', 'PS00003', 'ER03761', 'PS00004', 'ER03762', 'PS00001', 'PS00002', 'ER03544', 'ER04021', 'ER04020', 'ER04165', 'ER04085']:
        for j in extract_list:
             if i in j[1]:
                 ordered_extract_list_new.append(j)
                 break
    ordered_extract_list = ordered_extract_list_new
    patset = set()
    with open('extract_file.tsv', 'w') as ef:
        for extracts in ordered_extract_list:
            i = extracts[1]
            for j in snv_base_dict:
                if i[1].split('.')[0] in j:
                    seq = snv_base_dict[j]
            try:
                pat, time = extract_to_pat_and_time[i]
                patset.add(pat)
                time_since_start = time - datetime.datetime(2014, 1, 1)
                ef.write(i + '\t' + seq + '\t' + pat + '\t' + str(time_since_start.total_seconds()) + '\n')
            except:
                print i
    with open('pat_file.tsv', 'w') as pf:
        for i in patset:
            the_start = float('inf')
            the_end = 0
            for j in pat_dict[i].stays:
                start, end = j[:2]
                time_since_start = start - datetime.datetime(2014, 1, 1)
                if time_since_start.total_seconds() < the_start:
                    the_start = time_since_start.total_seconds()
                time_since_start = end - datetime.datetime(2014, 1, 1)
                if time_since_start.total_seconds() > the_end:
                    the_end = time_since_start.total_seconds()
            pf.write(i + '\t' + str(the_start) + '\t' + str(the_end) + '\n')
    new_bases = {}
    trans_oel = {}
    for i in ordered_extract_list:
        for j in snv_base_dict:
            if i[1].split('.')[0] in j:
                base_length = len(snv_base_dict[j])
                new_bases[j] = ''
                trans_oel[i[1]] = j
    new_pos_list = []
    for i in range(base_length):
        pos_base = []
        for j in ordered_extract_list:
            pos_base.append(snv_base_dict[trans_oel[j[1]]][i])
        if len(set(pos_base)) > 1:
            for j in ordered_extract_list:
                new_bases[trans_oel[j[1]]] += snv_base_dict[trans_oel[j[1]]][i]
            new_pos_list.append(snv_pos_list[i])
    snv_pos_list = new_pos_list
    snv_base_dict = new_bases


    for num, i in enumerate(ordered_extract_list):
        time, id = i
        x = get_x_time(time, start_dt, end_dt, width)
        # svg.drawLine(left_buffer + x, top_buffer - 10, left_buffer + x, top_buffer + (len(pat_dict) + 1) * pat_height, 3, cl=(0,0,255))
        newx = (num + 0.5) * width / len(extract_list)
        # svg.drawLine(left_buffer + x, top_buffer + (len(pat_dict) + 1) * pat_height, left_buffer + newx, top_buffer + (len(pat_dict) + 4) * pat_height, 3, cl=(0,0,255))
        date = time.isoformat()[:10]
        svg.writeString(id + ' - ' + date, left_buffer + newx - font_size/2, top_buffer + (len(pat_dict) + 4) * pat_height + 5, font_size, rotate=-1)
        for j in snv_base_dict:
            if id.split('.')[0] in j:
                bases = snv_base_dict[j]
        sw = 40
        max_pos = max(snv_pos_list)
        for q in ordered_extract_list[num+1:]:
            for j in snv_base_dict:
                if q[1].split('.')[0] in j:
                    bases2 = snv_base_dict[j]
            count = 0
            for i in range(len(bases)):
                if bases[i] != bases2[i]:
                    count += 1
        if num == 0:
            svg.drawOutRect(left_buffer - 120, top_buffer + (len(pat_dict) + 11) * pat_height + 5, 50, len(bases) * sw, lt=4, alpha2=0)
        for pos, j in enumerate(bases):
            the_pos = snv_pos_list[pos]
            if num == 0:
                x_coords = [left_buffer - 120, left_buffer - 70, left_buffer - 30, left_buffer - 10]
                yc1 = top_buffer + (len(pat_dict) + 11) * pat_height + 5 + the_pos * 1.0 / max_pos * len(bases) * sw
                yc2 = top_buffer + (len(pat_dict) + 11) * pat_height + 5 + pos * sw + sw/2
                y_coords = [yc1, yc1, yc2, yc2]
                svg.drawPath(x_coords, y_coords, th=4)
            svg.drawOutRect(left_buffer + newx - width / len(extract_list)/2, top_buffer + (len(pat_dict) + 11) * pat_height + 5 + pos * sw, width / len(extract_list) - 2, sw-2, fill=base_col[j], lt=0)
        svg.writeString(strain_to_name_dict[id], left_buffer + newx - font_size/2, top_buffer + (len(pat_dict) + 12) * pat_height + 5 + pos * sw, font_size, rotate=-1)

    leg_start = 7000
    hosp_enc_loc = list(loc_color)
    hosp_enc_loc.sort()
    for num, i in enumerate(hosp_enc_loc):
        if i in loc_color:
            if i.isdigit():
                svg.drawOutRect(left_buffer, leg_start + pat_height * num, stay_height * 2, stay_height, fill=loc_color[i], lt=0)
            else:
                svg.drawPatternRect(left_buffer, leg_start + pat_height * num, stay_height * 2, stay_height, i, fill=loc_color[i], lt=2)
            svg.writeString(i, left_buffer + stay_height * 2 + 10, leg_start + pat_height * num + stay_height, font_size)
    leg_dict = {'Outbreak A':(120,17,174), 'Outbreak B':(82,222,228), 'Outbreak C':(102,239,85), 'Precursor isolates':(250,150,50), 'Unrelated':(0,102,255), 'Culture negative':(255,255,255)}
    leg_list = list(leg_dict)
    leg_list.sort()
    for num, i in enumerate(leg_list):
        svg.drawOutRect(left_buffer + 1000, leg_start + pat_height * num, stay_height, stay_height, fill=leg_dict[i], lt=0)
        svg.writeString(i, left_buffer + stay_height * 1 + 10 + 1000, leg_start + pat_height * num + stay_height, font_size)
    symbol_dict = {'Surveillance culture':'s', 'Bacteremia culture':'o', 'Environmental culture':'u', 'Missing isolate':'x'}
    for num, i in enumerate(symbol_dict):
        svg.drawSymbol(left_buffer + 2000, leg_start + pat_height * num + pat_height/3, 30, (100,100,100), symbol_dict[i])
        svg.writeString(i, left_buffer + stay_height * 1 + 10 + 2000, leg_start + pat_height * num + stay_height, font_size)
    with open(vent_data) as f:
        f.readline()
        vent_dict = {}
        last_vent = None
        for line in f:
            vent, patient, dateandtime, date, time  = line.rstrip().split('\t')
            if last_vent != vent:
                if not last_vent is None:
                    vent_dict[last_vent].append(last_date)
                if not vent in vent_dict:
                    vent_dict[vent] = []
                vent_dict[vent].append(patient)
                vent_dict[vent].append(get_time(date))
            elif last_patient != patient:
                if last_date == vent_dict[vent][-1]:
                    last_date += datetime.timedelta(hours=24)
                vent_dict[vent].append(last_date)
                vent_dict[vent].append(patient)
                vent_dict[vent].append(get_time(date))
            last_date = get_time(date)
            last_patient = patient
            last_vent = vent
        if last_date == vent_dict[vent][-1]:
            last_date += datetime.timedelta(hours=24)
        vent_dict[vent].append(last_date)
    col_list = [[197,63,51],
[123,66,192],
[73,111,58],
[166,57,116],
[132,81,48],
[88,88,142]]
    svg.writesvg('shite.svg')
    svg = scalableVectorGraphics(height, width + left_buffer + right_buffer)
    for col_num, i in enumerate(vent_dict):
        print i
        color = col_list[col_num]
        to_draw = []
        last_pat = None
        last_x2 = None
        for j in range(0, len(vent_dict[i]), 3):
            loc, start, end = vent_dict[i][j:j+3]
            x1 = get_x_time(start, start_dt, end_dt, width) + left_buffer
            x2 = get_x_time(end, start_dt, end_dt, width) + left_buffer
            if loc == 'NICU':
                if last_x2 is None:
                    last_x2 = x1
                to_draw.append([last_x2, x2, 'nicu'])
            elif loc == 'OTHER' or not loc in y_axis_dict:
                if last_x2 is None:
                    last_x2 = x1
                to_draw.append([last_x2, x2, 'other'])
            else:
                if to_draw != []:
                    to_draw[-1][1] = x1
                    if last_pat is None:
                        last_pat = loc
                    y1 = y_axis_dict[last_pat]
                    y2 = y_axis_dict[loc]
                    start_x = to_draw[0][0]
                    end_x = to_draw[-1][1]
                    for k in to_draw:
                        if k[2] == 'other':
                            dash_pattern = (20, 10, 8, 10)
                        else:
                            dash_pattern = (12, 6, 12, 6)
                        the_y1 = (k[0] - start_x) * 1.0 / (end_x - start_x) * (y2 - y1) + y1
                        the_y2 = (k[1] - start_x) * 1.0 / (end_x - start_x) * (y2 - y1) + y1
                        svg.drawDash(k[0], the_y1, k[1], the_y2, 5, dash_pattern, color)
                        #
                        # if k[0] <= transisition < k[1]:
                        #     # svg.drawDash(k[0], y1, transisition, y1, 5, dash_pattern)
                        #     # svg.drawDash(transisition, y1,transisition, y2, 5, dash_pattern)
                        #     # svg.drawDash(transisition, y2, k[1], y2, 5, dash_pattern)
                        #     svg.drawDash(k[0], y1,k[1], y2, 5, dash_pattern)
                        # elif k[0] >= transisition:
                        #     svg.drawDash(k[0], y2, k[1], y2, 5, dash_pattern)
                        # elif k[0] <= transisition:
                        #     svg.drawDash(k[0], y1, k[1], y1, 5, dash_pattern)
                elif not last_pat is None:
                    svg.drawLine(last_x2, y_axis_dict[last_pat], x1, y_axis_dict[loc], 10, color)
                svg.drawLine(x1, y_axis_dict[loc], x2, y_axis_dict[loc], 10, color)
                last_pat = loc
                to_draw = []
            last_x2 = x2



    # for num, i in enumerate(other_loc2):
    #     svg.drawOutRect(left_buffer + 1000, leg_start + pat_height * num, stay_height, stay_height, fill=loc_color[i], lt=0)
    #     svg.writeString(i, left_buffer + stay_height * 1 + 10 + 1000, leg_start + pat_height * num + stay_height, font_size)


    # for num, i in enumerate(event_dict):
    #     svg.drawSymbol(left_buffer + 2000, leg_start + pat_height * num + pat_height/3, 30, (100,100,100), event_dict[i], lt=0)
    #     svg.writeString(i, left_buffer + stay_height * 1 + 10 + 2000, leg_start + pat_height * num + stay_height, font_size)
    # for num, i in enumerate(ab_color):
    #     svg.drawOutRect(left_buffer + 2500, leg_start + pat_height * num, stay_height, stay_height, fill=ab_color[i], lt=0)
    #     svg.writeString(i, left_buffer + stay_height * 1 + 10 + 2500, leg_start + pat_height * num + stay_height, font_size)
    # for num, i in enumerate(base_col):
    #     svg.drawOutRect(left_buffer + width + 20,  top_buffer + (len(pat_dict) + 11) * pat_height + 5 + num * stay_height, stay_height * 2, stay_height, fill=base_col[i], lt=0)
    #     svg.writeString(i, left_buffer + width + 40 + stay_height*2, top_buffer + (len(pat_dict) + 11) * pat_height + 5 + num * stay_height + stay_height, font_size)




    svg.writesvg(outfile)



pat_dict, pat_order = load_patients(sys.argv[1])
hosp_enc_loc, other_loc, encounter_span = get_events(pat_dict, sys.argv[2])
print hosp_enc_loc
get_antibiotics(pat_dict, sys.argv[3])
try:
    start_time = get_time(sys.argv[6])
except IndexError:
    start_time = encounter_span[0]
try:
    end_time = get_time(sys.argv[7])
except IndexError:
    end_time = encounter_span[1]

new_locs = add_fine_loc(pat_dict, sys.argv[8])
new_locs.add('NICU')
new_locs = list(new_locs)
new_locs.sort()
colors = [[160,87,58],
[199,77,175],
[228,136,44],
[211,130,186],
[173,106,34],
[214,68,134],
[213,158,93],
[152,69,104],
[215,80,44],
[222,123,139],
[142,99,46],
[217,62,93],
[231,141,109],
[180,66,57]]
c2 = [[165,102,201],
(80, 143, 61),
(131, 194, 112),
(53, 63, 177),
[137, 144, 220],
[151, 141, 53],
[202, 192, 104],
(141, 169, 216),
(52, 89, 152),
[90, 106, 47],
[151, 177, 78],
[76,178,148]]
count = 0
count2 = 0
for i in new_locs:
    if not i.isdigit() and i != 'NICU' and i != 'PICU':
        print '"' + i + '":' + '(' + ','.join(map(str, colors[count])) + '),'
        count += 1
    else:
        print '"' + i + '":' + '(' + ','.join(map(str, c2[count2])) + '),'
        count2 += 1


for i in new_locs:
    hosp_enc_loc.add(i)


snv_file = sys.argv[5]
vent_data = sys.argv[9]
draw_timeline(pat_dict, pat_order, sys.argv[4], hosp_enc_loc, other_loc, snv_file, vent_data, (start_time, end_time))