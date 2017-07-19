#!/usr/bin/env python
# draw_coloured_tree.py   Written by: Mitchell Sullivan   mjsull@gmail.com
# organisation: Icahn School of Medicine - Mount Sinai
# Version 0.0.1 2016.01.19
# License: GPLv3

from ete3 import Tree, RectFace, AttrFace, TextFace
import sys
from ete3 import NodeStyle
from ete3 import TreeStyle
from ete3 import Face
import argparse
import struct
import datetime



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
        self.out += '  <line x1="%d" y1="%d" x2="%d" y2="%d"\n        stroke-width="%d" stroke="%s" stroke-opacity="%f" stroke-linecap="round" />\n' % (x1, y1, x2, y2, th, colorstr(cl), alpha)

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

    def drawDash(self, x1, y1, x2, y2, exont):
        self.out += '  <line x1="%d" y1="%d" x2="%d" y2="%d"\n' % (x1, y1, x2, y2)
        self.out += '       style="stroke-dasharray: 5, 3, 9, 3"\n'
        self.out += '       stroke="#000" stroke-width="%d" />\n' % exont

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



def colorstr(rgb):
    return "#%02x%02x%02x" % (rgb[0],rgb[1],rgb[2])

def strtorgb(rgbstr):
    return struct.unpack('BBB',rgbstr[1:].decode('hex'))

# take a hue, saturation and lightness value and return a RGB hex string
def hsl_to_str(h, s, l):
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
    return "#%02x%02x%02x" % (r,g,b)

# main function for drawing tree
def draw_tree(the_tree, colour, label, out_file, the_scale, extend, bootstrap, group_file, grid_options, the_table):
    t = Tree(the_tree)
#    t.ladderize()

    o = t.get_midpoint_outgroup()
    t.set_outgroup(o)
    the_leaves = []
    for leaves in t.iter_leaves():
        the_leaves.append(leaves)
    groups = {}
    num = 0
    # set cutoff value for clades as 1/20th of the distance between the furthest two branches
    clade_cutoff = t.get_distance(the_leaves[0], the_leaves[-1]) /200
    # assign nodes to groups
    last_node = None
    ca_list = []
    if not group_file is None:
        with open(group_file) as f:
            group_dict = {}
            for line in f:
                group_dict[line.split()[0]] = line.split()[1]
        for node in the_leaves:
            i = node.name
            for j in group_dict:
                if j in i:
                    if j in groups:
                        groups[j].append(i)
                    else:
                        groups[j] = [i]
        for i in groups:
            the_col = group_dict[i]
            style = NodeStyle()
            style['size'] = 0
            style["vt_line_color"] = the_col
            style["hz_line_color"] = the_col
            style["vt_line_width"] = 2
            style["hz_line_width"] = 2
            if len(groups[i]) == 1:
                ca = t.search_nodes(name=groups[i])[0]
                ca.set_style(style)
            else:
                ca = t.get_common_ancestor(groups[i])
                ca.set_style(style)
                tocolor = []
                for j in ca.children:
                    tocolor.append(j)
                while len(tocolor) > 0:
                    x = tocolor.pop(0)
                    x.set_style(style)
                    for j in x.children:
                        tocolor.append(j)
            ca_list.append((ca, the_col))
        # for each common ancestor node get it's closest common ancestor neighbour and find the common ancestor of those two nodes
        # colour the common ancestor then add it to the group - continue until only the root node is left
        while len(ca_list) > 1:
            distance = float('inf')
            for i, col1 in ca_list:
                for j, col2 in ca_list:
                    if not i is j:
                        parent = t.get_common_ancestor(i, j)
                        getit = True
                        for children in parent.children:
                            if children != i and children != j:
                                getit = False
                                break
                        if getit:
                            the_dist = t.get_distance(i, j)
                            if the_dist <= distance:
                                distance = the_dist
                                the_i = i
                                the_j = j
                                the_i_col = col1
                                the_j_col = col2
            ca_list.remove((the_i, the_i_col))
            ca_list.remove((the_j, the_j_col))
            rgb1 = strtorgb(the_i_col)
            rgb2 = strtorgb(the_j_col)
            rgb3 = ((rgb1[0] + rgb2[0])/2, (rgb1[1] + rgb2[1])/2, (rgb1[2] + rgb2[2])/2)
            new_col = colorstr(rgb3)
            new_node = t.get_common_ancestor(the_i, the_j)
            the_col = new_col
            style = NodeStyle()
            style['size'] = 0
            style["vt_line_color"] = the_col
            style["hz_line_color"] = the_col
            style["vt_line_width"] = 2
            style["hz_line_width"] = 2
            new_node.set_style(style)
            ca_list.append((new_node, new_col))

    else:
        for node in the_leaves:
            i = node.name
            if not last_node is None:
                if t.get_distance(node, last_node) <= clade_cutoff:
                    groups[group_num].append(i)
                else:
                    groups[num] = [num, i]
                    group_num = num
                    num += 1
            else:
                groups[num] = [num, i]
                group_num = num
                num += 1
            last_node = node

    # Colour each group and then get the common ancestor node of each group
    if colour and group_file is None:
        for i in groups:
            num = groups[i][0]
            h = num * 360/len(groups)
            the_col = hsl_to_str(h, 0.5, 0.5)
            style = NodeStyle()
            style['size'] = 0
            style["vt_line_color"] = the_col
            style["hz_line_color"] = the_col
            style["vt_line_width"] = 2
            style["hz_line_width"] = 2
            if len(groups[i]) == 2:
                ca = t.search_nodes(name=groups[i][1])[0]
                ca.set_style(style)
            else:
                ca = t.get_common_ancestor(groups[i][1:])
                ca.set_style(style)
                tocolor = []
                for j in ca.children:
                    tocolor.append(j)
                while len(tocolor) > 0:
                    x = tocolor.pop(0)
                    x.set_style(style)
                    for j in x.children:
                        tocolor.append(j)
            ca_list.append((ca, h))
        # for each common ancestor node get it's closest common ancestor neighbour and find the common ancestor of those two nodes
        # colour the common ancestor then add it to the group - continue until only the root node is left
        while len(ca_list) > 1:
            distance = float('inf')
            got_one = False
            for i, col1 in ca_list:
                for j, col2 in ca_list:
                    if not i is j:
                        parent = t.get_common_ancestor(i, j)
                        getit = True
                        for children in parent.children:
                            if children != i and children != j:
                                getit = False
                                break
                        if getit:
                            the_dist = t.get_distance(i, j)
                            if the_dist <= distance:
                                distance = the_dist
                                the_i = i
                                the_j = j
                                the_i_col = col1
                                the_j_col = col2
                                got_one = True
            if not got_one:
                break
            ca_list.remove((the_i, the_i_col))
            ca_list.remove((the_j, the_j_col))
            new_col = (the_i_col + the_j_col) / 2
            new_node = t.get_common_ancestor(the_i, the_j)
            the_col = hsl_to_str(new_col, 0.5, 0.3)
            style = NodeStyle()
            style['size'] = 0
            style["vt_line_color"] = the_col
            style["hz_line_color"] = the_col
            style["vt_line_width"] = 2
            style["hz_line_width"] = 2
            new_node.set_style(style)
            ca_list.append((new_node, new_col))
    # if you just want a black tree
    elif group_file is None:
        style = NodeStyle()
        style['size'] = 0
        style["vt_line_color"] = '#000000'
        style["hz_line_color"] = '#000000'
        style["vt_line_width"] = 1
        style["hz_line_width"] = 1
        for n in t.traverse():
            n.set_style(style)
    svg = scalableVectorGraphics(2000, 5000)
    color_list = [(240,163,255),(0,117,220),(153,63,0),(76,0,92),(25,25,25),(0,92,49),(43,206,72),(255,204,153),
                  (128,128,128),(148,255,181),(143,124,0),(157,204,0),(194,0,136),(0,51,128),(255,164,5),(255,168,187),
                  (66,102,0),(255,0,16),(94,241,242),(0,153,143),(224,255,102),(116,10,255),(153,0,0),(255,255,128),
                  (255,255,0),(255,80,5), (0, 0, 0), (50, 50, 50)]
    up_to_colour = {}
    if not grid_options is None:
        column_list = []
        colour_dict = {}
        type_dict = {}
        width_dict = {}
        min_val_dict = {}
        max_val_dict = {}
        leaf_name_dict = {}
        header_count = 0
        the_columns = {}
        if grid_options == 'auto':
            with open(the_table) as f:
                headers = f.readline().rstrip().split('\t')[1:]
                for i in headers:
                    the_columns[i] = [i]
                    type_dict[i] = 'colour'
                    colour_dict[i] = {'empty':'#FFFFFF'}
                    width_dict[i] = 20
                    up_to_colour[i] = 0
                    column_list.append(i)
        else:
            with open(grid_options) as g:
                for line in g:
                    if line.startswith('H'):
                        print line
                        name, type, width = line.rstrip().split('\t')[1:]
                        if name in the_columns:
                            the_columns[name].append(name + '_' + str(header_count))
                        else:
                            the_columns[name] = [name + '_' + str(header_count)]
                        width = int(width)
                        name = name + '_' + str(header_count)
                        header_count += 1
                        colour_dict[name] = {'empty':'#FFFFFF'}
                        type_dict[name] = type
                        width_dict[name] = width
                        column_list.append(name)
                        up_to_colour[name] = 0
                        min_val_dict[name] = float('inf')
                        max_val_dict[name] = 0
                    elif line.startswith('C'):
                        c_name, c_col = line.rstrip().split('\t')[1:]
                        if not c_col.startswith('#'):
                            c_col = colorstr(map(int, c_col.split(',')))
                        colour_dict[name][c_name] = c_col
        val_dict = {}
        with open(the_table) as f:
            headers = f.readline().rstrip().split('\t')[1:]
            column_no = {}
            for num, i in enumerate(headers):
                if i in the_columns:
                    column_no[num] = i
            for line in f:
                name = line.split('\t')[0]
                leaf_name = None
                for n in t.traverse():
                    if n.is_leaf():
                        if name.split('.')[0] in n.name:
                            leaf_name = n.name
                if leaf_name is None:
                    continue
                else:
                    leaf_name_dict[leaf_name] = name
                vals = line.rstrip().split('\t')[1:]
                if name in val_dict:
                    sys.exit('Duplicate entry found in table.')
                else:
                    val_dict[name] = {}
                for num, val in enumerate(vals):
                    if num in column_no and val != '':
                        for q in the_columns[column_no[num]]:
                            column_name = q
                            if type_dict[column_name] == 'colour':
                                val_dict[name][column_name] = val
                                if not val in colour_dict[column_name]:
                                    colour_dict[column_name][val] = colorstr(color_list[up_to_colour[column_name] % len(color_list)])
                                    up_to_colour[column_name] += 1
                            elif type_dict[column_name] == 'text':
                                val_dict[name][column_name] = val
                            elif type_dict[column_name] == 'colour_scale_date':
                                year, month, day = val.split('-')
                                year, month, day = int(year), int(month), int(day)
                                the_val = datetime.datetime(year, month, day, 0, 0, 0) - datetime.datetime(1970, 1, 1, 0, 0, 0)
                                val_dict[name][column_name] = the_val.total_seconds()
                                if the_val.total_seconds() < min_val_dict[column_name]:
                                    min_val_dict[column_name] = the_val.total_seconds()
                                if the_val.total_seconds() > max_val_dict[column_name]:
                                    max_val_dict[column_name] = the_val.total_seconds()
                            elif type_dict[column_name] == 'colour_scale':
                                the_val = float(val)
                                val_dict[name][column_name] = the_val
                                if the_val < min_val_dict[column_name]:
                                    min_val_dict[column_name] = the_val
                                if the_val > max_val_dict[column_name]:
                                    max_val_dict[column_name] = the_val
                            else:
                                sys.exit('Unknown column type')
        new_desc = open(out_file + '.new_desc', 'w')
        for num, i in enumerate(column_list):
            new_desc.write('H\t' + i.rsplit('_', 1)[0] + '\t' + type_dict[i] + '\t' + str(width_dict[i]) + '\n')
            x = num * 200
            svg.writeString(i, x+50, 20, 12)
            if type_dict[i] == 'colour':
                for num2, j in enumerate(colour_dict[i]):
                    new_desc.write('C\t' + j + '\t' + colour_dict[i][j] + '\n')
                    y = num2 * 20 + 30
                    svg.drawOutRect(x + 50, y, 12, 12, strtorgb(colour_dict[i][j]), strtorgb(colour_dict[i][j]), lt=0)
                    svg.writeString(j, x + 70, y + 12, 12)
            elif type_dict[i] == 'colour_scale':
                for num2 in range(11):
                    y = num2 * 20 + 30
                    val = (max_val_dict[i] - min_val_dict[i]) * num2 / 10.0
                    h = val / (max_val_dict[i] - min_val_dict[i]) * 360
                    s = 0.5
                    l = 0.5
                    colour = hsl_to_str(h, s, l)
                    svg.drawOutRect(x + 50, y, 12, 12, strtorgb(colour), strtorgb(colour), lt=0)
                    svg.writeString(str(val), x + 70, y + 12, 12)
            elif type_dict[i] == 'colour_scale_date':
                for num2 in range(11):
                    y = num2 * 20 + 30
                    val = (max_val_dict[i] - min_val_dict[i]) * num2 / 10.0
                    h = val / (max_val_dict[i] - min_val_dict[i]) * 360
                    s = 0.5
                    l = 0.5
                    colour = hsl_to_str(h, s, l)
                    days = str(int(val / 60/ 60/ 24)) + ' days'
                    svg.drawOutRect(x + 50, y, 12, 12, strtorgb(colour), strtorgb(colour), lt=0)
                    svg.writeString(days, x + 70, y + 12, 12)
            for n in t.traverse():
                if n.is_leaf():
                    name = leaf_name_dict[n.name]
                    if i in val_dict[name]:
                        val = val_dict[name][i]
                    else:
                        val = 'empty'
                    if type_dict[i] == 'colour':
                        print 'ding'
                        n.add_face(RectFace(width_dict[i], 20, colour_dict[i][val], colour_dict[i][val]), column=num+1, position="aligned")
                    elif type_dict[i] == 'colour_scale' or type_dict[i] == 'colour_scale_date':
                        if val == 'empty':
                            colour = '#FFFFFF'
                        else:
                            h = (val - min_val_dict[i]) / (max_val_dict[i] - min_val_dict[i]) * 360
                            s = 0.5
                            l = 0.5
                            colour = hsl_to_str(h, s, l)
                        n.add_face(RectFace(width_dict[i], 20, colour, colour), column=num+1, position="aligned")
                    elif type_dict[i] == 'text':
                        n.add_face(TextFace(val, fsize=12), column=num+1, position="aligned")

    ts = TreeStyle()
    # Set these to False if you don't want bootstrap/distance values
    ts.show_branch_length = label
    ts.show_branch_support = bootstrap
    ts.show_leaf_name = False
    for node in t.traverse():
        if node.is_leaf():
            node.add_face(AttrFace("name", fsize=6, fgcolor='black'), column=0, position="aligned")
    ts.margin_left = 20
    ts.margin_right = 100
    ts.margin_top = 20
    ts.margin_bottom = 20
    if extend:

        ts.draw_guiding_lines = True
    ts.scale = the_scale
    # ts.mode = "c"
    # ts.arc_start = 0
    # ts.arc_span = 360
    if out_file == 'inter':
        t.show(tree_style=ts)
    else:
        t.render(out_file, w=210, units='mm', tree_style=ts)
        svg.writesvg(out_file + '.leg.svg')


parser = argparse.ArgumentParser()
parser.add_argument("-o", "--output_svg", help="SVG of tree", metavar="tree.svg")
parser.add_argument("-n", "--newick", help="newick tree file", metavar="tree.nw")
parser.add_argument("-c", '--color', action="store_true", default=False, help="Color tree")
parser.add_argument("-l", '--label', action="store_true", default=False, help="Add distance values")
parser.add_argument("-b", '--bootstrap', action="store_true", default=False, help="add bootstrap values")
parser.add_argument("-s", "--scale", type=float, default=5000, help="x scale of tree")
parser.add_argument("-d", '--desc', help="add MLST types from pathogendb", metavar="assemblies.csv")
parser.add_argument("-t", '--tsv', help="add resistances from pathogendb", metavar="resistance.csv")
parser.add_argument("-g", '--group_file', help="file with groups of strains", metavar="Group.tsv")
parser.add_argument("-e", '--extend', help="extend tree branch", default=False, action="store_true")
args = parser.parse_args()

draw_tree(args.newick, args.color, args.label, args.output_svg, args.scale, args.extend, args.bootstrap, args.group_file, args.desc, args.tsv)
