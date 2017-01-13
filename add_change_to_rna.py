import sys
import urllib2
import os
import seaborn as sns
import numpy
import pandas


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
            self.out += '        xc="%d" yc="%d" r="%d" />\n' % (x, y, size/2)
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
    def writeString(self, thestring, x, y, size, ital=False, bold=False, rotate=0, justify='left', color=(0,0,0)):
        if rotate != 0:
            x, y = y, x
        self.out += '  <text\n'
        self.out += '    style="font-size:%dpx;font-style:normal;font-weight:normal;z-index:10\
;line-height:125%%;letter-spacing:0px;word-spacing:0px;fill:%s;fill-opacity:1;stroke:none;font-family:Sans"\n' % (size, colorstr(color))
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




def add_change(diff_file, gbk_file, out_file, the_number, the_pval, diff_list, go_dir, panel3):
    the_number, the_pval = int(the_number), float(the_pval)
    with open(diff_file) as diff:
        diff_dict = {}
        diff.readline()
        for line in diff:
            type, q_name, pos1, pos2, r_name, pos3, pos4, b1, b2, anc_type, mut_type, genes1, genes2, genes3, genes4, genes5, genes6, genes7, genes8, genes9, genes10 = line.rstrip().split('\t')
            if mut_type in ['nonsyn_query', 'nonsyn_query_stop', 'syn_query', 'inframe_del_query', 'deletion_query',
                            'inframe_ins_query', 'insertion_query', 'syn_amb', 'syn_ref', 'nonsyn_amb', 'nonsyn_amb_stop',
                            'nonsyn_ref', 'no_matching_genes']:
                genes = genes2.split(';')
                genes = filter(lambda a: a != 'none', genes)
                for i in genes:
                    loci = i.split(',')[1]
                    if loci in diff_dict:
                        diff_dict[loci] += ';' + mut_type
                    else:
                        diff_dict[loci] = mut_type
            elif mut_type in ['intergenic_ref', 'intergenic_amb', 'intergenic_query', 'no_matching_genes']:
                genes = genes8.split(';') + genes10.split(';')
                genes = filter(lambda a: a != 'none', genes)
                for i in genes:
                    loci = i.split(',')[1]
                    distance = i.split(',')[-1].split('/')[0][1:]
                    if loci in diff_dict:
                        diff_dict[loci] += ';upstream_mut,' + distance
                    else:
                        diff_dict[loci] = 'upstream_mut,' + distance
            elif mut_type == 'deletion in query' or mut_type == 'plasmid_loss':
                genes = genes2.split(';') + genes4.split(';')
                genes = filter(lambda a: a != 'none', genes)
                for i in genes:
                    loci = i.split(',')[1]
                    if loci in diff_dict:
                        diff_dict[loci] += ';partial_del'
                    else:
                        diff_dict[loci] = 'partial_del'
                genes = genes6.split(';')
                genes = filter(lambda a: a != 'none', genes)
                for i in genes:
                    loci = i.split(',')[1]
                    if loci in diff_dict:
                        diff_dict[loci] += ';' + mut_type
                    else:
                        diff_dict[loci] = mut_type
                genes = genes8.split(';') + genes10.split(';')
                genes = filter(lambda a: a != 'none', genes)
                for i in genes:
                    loci = i.split(',')[1]
                    distance = i.split(',')[-1].split('/')[0][1:]
                    if loci in diff_dict:
                        diff_dict[loci] += ';upstream_mut_del,' + distance
                    else:
                        diff_dict[loci] = 'upstream_mut_del,' + distance
            elif mut_type == 'tandem contraction in query':
                genes = genes2.split(';')
                genes = filter(lambda a: a != 'none', genes)
                for i in genes:
                    loci = i.split(',')[1]
                    if loci in diff_dict:
                        diff_dict[loci] += ';Tandem contraction'
                    else:
                        diff_dict[loci] = 'Tandem contraction'
                genes = genes8.split(';') + genes10.split(';')
                genes = filter(lambda a: a != 'none', genes)
                for i in genes:
                    loci = i.split(',')[1]
                    distance = i.split(',')[-1].split('/')[0][1:]
                    if loci in diff_dict:
                        diff_dict[loci] += ';upstream_mut_cont,' + distance
                    else:
                        diff_dict[loci] = 'upstream_mut_cont,' + distance
            elif mut_type == 'deletion in query (duplicated ends)':
                genes = genes2.split(';') + genes4.split(';')
                genes = filter(lambda a: a != 'none', genes)
                for i in genes:
                    loci = i.split(',')[1]
                    if loci in diff_dict:
                        diff_dict[loci] += ';partial_del'
                    else:
                        diff_dict[loci] = 'partial_del'
                genes = genes6.split(';')
                genes = filter(lambda a: a != 'none', genes)
                for i in genes:
                    loci = i.split(',')[1]
                    if loci in diff_dict:
                        diff_dict[loci] += ';deletion in query'
                    else:
                        diff_dict[loci] = 'deletion in query'
                genes = genes8.split(';') + genes10.split(';')
                genes = filter(lambda a: a != 'none', genes)
                for i in genes:
                    loci = i.split(',')[1]
                    distance = i.split(',')[-1].split('/')[0][1:]
                    if loci in diff_dict:
                        diff_dict[loci] += ';upstream_mut_del,' + distance
                    else:
                        diff_dict[loci] = 'upstream_mut_del,' + distance
            elif mut_type == 'tandem expansion in query':
                genes = genes2.split(';')
                genes = filter(lambda a: a != 'none', genes)
                for i in genes:
                    loci = i.split(',')[1]
                    if loci in diff_dict:
                        diff_dict[loci] += ';Tandem expansion'
                    else:
                        diff_dict[loci] = 'Tandem expansion'
                genes = genes8.split(';') + genes10.split(';')
                genes = filter(lambda a: a != 'none', genes)
                for i in genes:
                    loci = i.split(',')[1]
                    distance = i.split(',')[-1].split('/')[0][1:]
                    if loci in diff_dict:
                        diff_dict[loci] += ';upstream_mut_exp,' + distance
                    else:
                        diff_dict[loci] = 'upstream_mut_exp,' + distance
            elif mut_type == 'insertion in query' or mut_type == 'plasmid_gain':
                genes = genes2.split(';') + genes4.split(';')
                genes = filter(lambda a: a != 'none', genes)
                for i in genes:
                    loci = i.split(',')[1]
                    if loci in diff_dict:
                        diff_dict[loci] += ';partial insertion,'
                    else:
                        diff_dict[loci] = 'partial insertion'
                genes = genes6.split(';')
                genes = filter(lambda a: a != 'none', genes)
                for i in genes:
                    loci = i.split(',')[1]
                    if loci in diff_dict:
                        diff_dict[loci] += ';' + mut_type
                    else:
                        diff_dict[loci] = mut_type
                genes = genes8.split(';') + genes10.split(';')
                genes = filter(lambda a: a != 'none', genes)
                for i in genes:
                    loci = i.split(',')[1]
                    distance = i.split(',')[-1].split('/')[0][1:]
                    if loci in diff_dict:
                        diff_dict[loci] += ';upstream_mut_ins,' + distance
                    else:
                        diff_dict[loci] = 'upstream_mut_ins,' + distance
            elif mut_type == 'insertion in query (duplicated ends)':
                genes = genes2.split(';') + genes4.split(';')
                genes = filter(lambda a: a != 'none', genes)
                for i in genes:
                    loci = i.split(',')[1]
                    if loci in diff_dict:
                        diff_dict[loci] += ';partial insertion'
                    else:
                        diff_dict[loci] = 'partial insertion'
                genes = genes6.split(';')
                genes = filter(lambda a: a != 'none', genes)
                for i in genes:
                    loci = i.split(',')[1]
                    if loci in diff_dict:
                        diff_dict[loci] += ';' + mut_type
                    else:
                        diff_dict[loci] = mut_type
                genes = genes8.split(';') + genes10.split(';')
                genes = filter(lambda a: a != 'none', genes)
                for i in genes:
                    loci = i.split(',')[1]
                    distance = i.split(',')[-1].split('/')[0][1:]
                    if loci in diff_dict:
                        diff_dict[loci] += ';upstream_mut_ins,' + distance
                    else:
                        diff_dict[loci] = 'upstream_mut_ins,' + distance
            elif mut_type == 'inversion':
                genes = genes2.split(';')
                genes = filter(lambda a: a != 'none', genes)
                for i in genes:
                    loci = i.split(',')[1]
                    if loci in diff_dict:
                        diff_dict[loci] += ';inverted'
                    else:
                        diff_dict[loci] = 'inverted'
                genes = genes6.split(';')
                genes = filter(lambda a: a != 'none', genes)
                for i in genes:
                    loci = i.split(',')[1]
                    if loci in diff_dict:
                        diff_dict[loci] += ';' + mut_type
                    else:
                        diff_dict[loci] = mut_type
                genes = genes8.split(';') + genes10.split(';')
                genes = filter(lambda a: a != 'none', genes)
                for i in genes:
                    loci = i.split(',')[1]
                    distance = i.split(',')[-1].split('/')[0][1:]
                    if loci in diff_dict:
                        diff_dict[loci] += ';upstream_mut_inv,' + distance
                    else:
                        diff_dict[loci] = 'upstream_mut_inv,' + distance
            elif mut_type == 'Variable region':
                genes = genes2.split(';')
                genes = filter(lambda a: a != 'none', genes)
                for i in genes:
                    loci = i.split(',')[1]
                    if loci in diff_dict:
                        diff_dict[loci] += ';gene modified'
                    else:
                        diff_dict[loci] = 'gene modified'
            else:
                print mut_type, 'dong dong dong'
    gene_dict = {}
    loc_dict = {}
    loc_lengths = []
    gap_bp = 20000
    with open(gbk_file) as gbk:
        for line in gbk:
            line = line.rstrip()
            if line.startswith('LOCUS'):
                chrom = line.split()[1]
                loc_lengths.append((int(line.split()[2]), chrom))
            if line.startswith('     CDS'):
                gene_name = 'none'
                description = 'Hypothetical protein'
                inference = 'none'
                loc = line.split()[1]
                if loc.startswith('complement'):
                    pos = int(loc.split('..')[0][11:])
                    dir = False
                else:
                    pos = int(loc.split('..')[0])
                    dir = True
            elif line.startswith('                     /gene="'):
                gene_name = line.split('"')[1].split('_')[0]
            elif line.startswith('                     /locus_tag="'):
                locus = line.split('"')[1]
            elif line.startswith('                     /inference="similar to AA sequence'):
                inference = line.split('"')[1].split(':')[-1]
            elif line.startswith('                     /inference="protein motif:Pfam:'):
                inference = line.split(':')[-1].split('.')[0]
            elif line.startswith('                     /product="'):
                description = line.split('"')[1]
            elif line.startswith('                     /translation="'):
                gene_dict[locus] = [gene_name, inference, description]
                loc_dict[locus] = (chrom, pos, dir)
    loc_starts = {}
    loc_lengths.sort(reverse=True)
    curr_length = 0
    for i in loc_lengths:
        loc_starts[i[1]] = curr_length
        curr_length += i[0] + gap_bp
    total_bp = curr_length - gap_bp
    new_loc_dict = {}
    dir_dict = {}
    for i in loc_dict:
        dir_dict[i] = loc_dict[i][2]
        new_loc_dict[i] = loc_starts[loc_dict[i][0]] + loc_dict[i][1]
    old_loc_dict = loc_dict
    loc_dict = new_loc_dict
    go_descriptions = {}
    gene_go = {}
    fam_acc = {}
    for i in diff_list[:the_number]:
        go_file = go_dir + '/' + i.split('/')[-1][:-7] + 'GO_GeneID.tsv'
        with open(go_file) as gf:
            gf.readline()
            for line in gf:
                tn, bp, sn, goid, term, annotated, signif, expected, pval, genesfound, score = line.split('\t')
                go_descriptions[goid[1:-1]] = term[1:-1]
                for i in genesfound[1:-1].split(','):
                    if i in gene_go:
                        gene_go[i].add(goid[1:-1])
                    else:
                        gene_go[i] = set([goid[1:-1]])


    # if not os.path.exists('this_is_an_rna_go_file'):
    #     online_mode = True
    #     out_go = open('this_is_an_rna_go_file', 'w')
    # else:
    #     online_mode = False
    #     tiagd = {}
    #     with open('this_is_an_rna_go_file') as tiagf:
    #         for line in tiagf:
    #             if line.split('\t')[0] in tiagd:
    #                 tiagd[line.split('\t')[0]].append(line.rstrip().split('\t')[1:])
    #             else:
    #                 tiagd[line.split('\t')[0]] = [line.rstrip().split('\t')[1:]]
    # print 'using online mode', online_mode
    # go_rel_dict = {}
    # with open('go.obo') as goobo:
    #     for line in goobo:
    #         if line.startswith('id: '):
    #             go = line.rstrip()[4:]
    #             go_rel_dict[go] = []
    #         elif line.startswith('is_a: '):
    #             go_rel_dict[go].append(line.split()[1])
    #         elif line.startswith('relationship: part_of'):
    #             go_rel_dict[go].append(line.split()[2])
    #         elif line.startswith('name: '):
    #             go_descriptions[go] = line.rstrip()[6:]
    # for i in gene_dict:
    #     if gene_dict[i][1].startswith('PF'):
    #         fam_acc[gene_dict[i][1]] = i
    #     elif gene_dict[i][1] != 'none':
    #         if online_mode:
    #             req = urllib2.urlopen('http://www.ebi.ac.uk/QuickGO/GAnnotation?protein=' + gene_dict[i][1] + '&format=tsv')
    #             print 'http://www.ebi.ac.uk/QuickGO/GAnnotation?protein=' + gene_dict[i][1] + '&format=tsv'
    #             req.readline()
    #             for line in req:
    #                 go, desc = line.split('\t')[6:8]
    #                 out_go.write(gene_dict[i][1] + '\t' + go + '\t' + desc + '\n')
    #                 if i in gene_go:
    #                     gene_go[i].add(go)
    #                 else:
    #                     gene_go[i] = set([go])
    #                 go_descriptions[go] = desc
    #             if not i in gene_go:
    #                 print i, 'http://www.uniprot.org/uniprot/' + gene_dict[i][1] + '.rdf'
    #                 req = urllib2.urlopen('http://www.uniprot.org/uniprot/' + gene_dict[i][1] + '.rdf')
    #                 new_accs = []
    #                 for line in req:
    #                     if line.startswith('<replacedBy rdf:resource='):
    #                         new_accs.append(line.split('"')[1].split('/')[-1])
    #                 print new_accs
    #                 if new_accs != []:
    #                     new_acc = new_accs[-1]
    #                     req = urllib2.urlopen('http://www.ebi.ac.uk/QuickGO/GAnnotation?protein=' + new_acc + '&format=tsv')
    #                     req.readline()
    #                     for line in req:
    #                         go, desc = line.split('\t')[6:8]
    #                         out_go.write(gene_dict[i][1] + '\t' + go + '\t' + desc + '\n')
    #                         if i in gene_go:
    #                             gene_go[i].add(go)
    #                         else:
    #                             gene_go[i] = set([go])
    #                         go_descriptions[go] = desc
    #         else:
    #             if gene_dict[i][1] in tiagd:
    #                 for j in tiagd[gene_dict[i][1]]:
    #                     go, desc = j
    #                     if i in gene_go:
    #                         gene_go[i].add(go)
    #                     else:
    #                         gene_go[i] = set([go])
    #                     go_descriptions[go] = desc
    # for i in gene_go:
    #     new_set = gene_go[i]
    #     old_set = set()
    #     while len(new_set) != len(old_set):
    #         old_set = new_set
    #         new_set = set()
    #         for j in old_set:
    #             new_set.add(j)
    #             try:
    #                 for k in go_rel_dict[j]:
    #                     new_set.add(k)
    #             except KeyError:
    #                 pass
    #     gene_go[i] = new_set
    # req = urllib2.urlopen('http://geneontology.org/external2go/pfam2go')
    # for line in req:
    #     if not line.startswith('!'):
    #         if line.split()[0].split(':')[1] in fam_acc:
    #             gene = line.split()[0].split(':')[1]
    #             go = line.split()[-1]
    #             desc = line.split(':')[2][:-5]
    #             go_descriptions[go] = desc
    #             if gene in gene_go:
    #                 gene_go[gene].add(go)
    #             else:
    #                 gene_go[gene] = set([go])
    rna_diff_dict = {}
    gene_list = set()
    rna_pval_dict = {}
    headers = []
    for num, rna_diff_file in enumerate(diff_list):
        headers.append(rna_diff_file.split('/')[-1])
        with open(rna_diff_file) as rna_diff:
            rna_diff.readline()
            for line in rna_diff:
                gene_name, chr, gene_length, gene_sym, type_of_gene, logfc, aveexp, tval, nonadj_pval, pval, bval = line.rstrip().split('\t')
                logfc, pval = float(logfc), float(pval)
                if gene_name in rna_diff_dict:
                    rna_diff_dict[gene_name].append(logfc)
                    rna_pval_dict[gene_name].append(pval)
                else:
                    if gene_name in loc_dict:
                        rna_diff_dict[gene_name] = [logfc]
                        rna_pval_dict[gene_name] = [pval]
                    # else:
                    #     print gene_name
                if not gene_name in gene_go:
                    gene_go[gene_name] = set([])

                if pval <= the_pval and num < the_number and gene_name in loc_dict:# and gene_dict[gene_name][2] != 'hypothetical protein':
                    # if gene_name in diff_dict:
                    #     print diff_dict[gene_name]
                    #     if diff_dict[gene_name] != 'full_del' and diff_dict[gene_name] != 'deletion in query' and diff_dict[gene_name] != 'plasmid_loss':
                    #         gene_list.add(gene_name)
                    # else:
                        gene_list.add(gene_name)
    combo_list = {}
    for i in rna_diff_dict:
        diff_it = []
        for j in range(len(rna_diff_dict[i])):
            if rna_pval_dict[i][j] < 0.05:
                if rna_diff_dict[i][j] < 0:
                    the_diff = 'up_query'
                else:
                    the_diff = 'up_reference'
            else:
                the_diff = 'no_change'
            diff_it.append(the_diff)
        diff_it = ','.join(diff_it)
        if diff_it in combo_list:
            combo_list[diff_it].append(i)
        else:
            combo_list[diff_it] = [i]
    with open(out_file + '.tsv', 'w') as groups:
        for j in diff_list:
            groups.write(j.split('/')[-1] + '\t')
        groups.write('Count\n')
        combo_list_list = list(combo_list)
        combo_list_list.sort()
        for i in combo_list_list:
            groups.write('\t'.join(i.split(',')) + '\t' + str(len(combo_list[i])) + '\n')
        groups.write('\n\n\n\n\n\n\n')
        for i in combo_list_list:
            groups.write('Comparison\tchange\n')
            for j, k in zip(diff_list, i.split(',')):
                groups.write(j.split('/')[-1] + '\t' + k + '\n')
            groups.write('LOCUS\tgene name\tdescription\tchange\n')
            combo_list[i].sort()
            for j in combo_list[i]:
                if j in diff_dict:
                    change = diff_dict[j]
                else:
                    change = 'none'
                groups.write(j + '\t' + gene_dict[j][0] + '\t' + gene_dict[j][2] + '\t' + change + '\n')
            groups.write('\n\n\n')
    gene_list = list(gene_list)
    gene_list.sort(key=lambda x: loc_dict[x])
    go_list = []
    go_set = set()
    for i in gene_list:
        for j in gene_go[i]:
            go_set.add(j)
    for i in go_set:
        go_list.append(i)
    #         if j in go_set:
    #             go_set[j] += 1
    #         else:
    #             go_set[j] = 1
    # go_gene_dict = {}
    # for i in go_list:
    #     gene_set = set()
    #     for j in gene_list:
    #         if j in gene_go and i in gene_go[j]:
    #             gene_set.add(j)
    #     go_gene_dict[i] = gene_set
    # go_groups = []
    # for i in go_gene_dict:
    #     gotit = False
    #     for j in go_groups:
    #         if j[1] == go_gene_dict[i]:
    #             j[0].append(i)
    #             gotit = True
    #             break
    #     if not gotit:
    #         go_groups.append([[i], go_gene_dict[i]])
    # go_list = []
    # for i in go_groups:
    #     parents = set()
    #     for j in i[0]:
    #         for k in go_rel_dict[j]:
    #             parents.add(k)
    #     print 'ding', len(i[0])
    #     for j in i[0]:
    #         if not j in parents:
    #             print j
    #             go_list.append(j)
    # for i in go_descriptions:
    #     if go_descriptions[i] == 'biological_process':
    #         parent_go = i
    # new_go_list = []
    # for i in go_list:
    #     new_set = set([i])
    #     old_set = set()
    #     while len(new_set) != len(old_set):
    #         old_set = new_set
    #         new_set = set()
    #         for j in old_set:
    #             new_set.add(j)
    #             try:
    #                 for k in go_rel_dict[j]:
    #                     new_set.add(k)
    #             except KeyError:
    #                 pass
    #     if parent_go in new_set:
    #         new_go_list.append(i)
    # print len(go_list)
    # go_list = new_go_list
    # print len(go_list)

    svg = scalableVectorGraphics(5000, 5000)
    the_array = numpy.zeros((len(gene_list), len(go_list)))
    for num1, i in enumerate(gene_list):
        for num2, j in enumerate(go_list):
            if j in gene_go[i]:
                the_array[num1][num2] = 1
    df = pandas.DataFrame(the_array)
    cluster = sns.clustermap(df, col_cluster=True, row_cluster=False)
    new_go_list = []
    for i in cluster.dendrogram_col.reordered_ind:
        new_go_list.append(go_list[i])
    go_list = new_go_list
    var_color = {
        'full_del':(217,70,42),#
        'deletion in query':(217,70,42),#

        'nonsyn_query':(215,64,146),

        'partial_del':(227,133,51),

        'syn_query':(87,198,57),
        'syn_ref':(87,198,57),
        'nonsyn_ref':(224,126,173),

        'deletion_query':(104,128,0),
        'insertion_query':(104,128,0),
        'plasmid_loss':(156,186,58),

        'promoter': (86,173,208),

        'mult':(148,110,209),

    }
    grid_start = 400
    square_height = 4
    square_width = 10
    top_buffer = 400
    for num, i in enumerate(headers):
        svg.writeString(i, 310 + num * square_width, top_buffer-10, 10, justify='right', rotate=-1)
    change_set = set()
    total_height = len(gene_list) * square_height
    for i in loc_lengths:
        length, chrom = i
        start = loc_starts[chrom]
        svg.drawOutRect(180, start * 1.0 / total_bp * total_height + top_buffer, 20, length * 1.0 / total_bp * total_height)
    last_loci = 'PROKKA_00000'
    opcolor = (100, 100, 200)
    gene_groups = []
    gene_group = []
    diff_in_group = False
    for num, i in enumerate(gene_list):
        if gene_dict[i][0] != 'none':
            gene_name = gene_dict[i][0]
        else:
            gene_name = i
        gene_desc = gene_dict[i][2]
        if int(last_loci.split('_')[1]) != int(i.split('_')[1]) - 1 or old_loc_dict[i][0] != old_loc_dict[last_loci][0]:
            switchit = True
            if not last_loci == 'PROKKA_00000' and dir_dict[last_loci] == dir_dict[i] and old_loc_dict[i][0] == old_loc_dict[last_loci][0]:
                switchit = False
                for j in range(int(last_loci.split('_')[1]) + 1, int(i.split('_')[1])):
                    if 'PROKKA_' + str(j).zfill(5) in dir_dict and dir_dict['PROKKA_' + str(j).zfill(5)] == dir_dict[i]:
                        switchit = True
                        break
            if switchit:
                x1 = 305 # grid_start + (len(rna_diff_dict[i]) + len(go_list) + 1) * square_width + 40
                if diff_in_group:
                    gene_groups.append(gene_group)
                gene_group = [(i, num)]
                diff_in_group = False
                if opcolor == (0, 100, 0):
                    opcolor = (100, 0, 100)
                else:
                    opcolor = (0, 100, 0)
            else:
                gene_group.append((i, num))
                x1 = 300
        else:
            gene_group.append((i, num))
            x1 = 300
        # svg.writeString(gene_name, grid_start - 10, top_buffer + num * square_height + 0.75 * square_height, 10, justify='right', color=opcolor)
        # svg.writeString(gene_desc, grid_start + (len(rna_diff_dict[i]) + len(go_list) + 1) * square_width + 45, top_buffer + num * square_height + 0.75 * square_height, 10, color=opcolor)
        y1 = loc_dict[i] * 1.0 / total_bp * total_height + top_buffer
        y2 = top_buffer + num * square_height + 0.3 * square_height
        last_loci = i
        svg.drawPath([180, 200, 280, x1], [y1, y1, y2, y2], th=1, cl=opcolor)
        if i in diff_dict:
            if ';' in diff_dict[i]:
                color = var_color['mult']
                diff_in_group = True
                change_set.add('mult')
            elif diff_dict[i].startswith('upstream'):
                dist = int(diff_dict[i].split(',')[1])
                change_set.add('promoter')
                if dist < 1000:
                    diff_in_group = True
                    color = var_color['promoter']
                else:
                    color = (220, 220, 220)
            else:
                diff_in_group = True
                try:
                    change_set.add(diff_dict[i])
                    color = var_color[diff_dict[i]]
                except:
                    print 'ding ding ding', diff_dict[i]
                    color = (255, 0, 0)
        else:
            color = (220, 220, 220)
        svg.drawOutRect(grid_start, top_buffer + square_height * num, 19, square_height - 1, lt=0, fill=color)
        for num2, j in enumerate(rna_diff_dict[i]):
            if j < 0:
                r = 1 - min([1, j / -3])
                color = hsl_to_rgb(0, 0.9, r/2 + 0.5)
            else:
                b = 1 - min([1, j / 3])
                color = hsl_to_rgb(250, 0.9, b/2 + 0.5)
            svg.drawOutRect(310 + num2 * square_width, top_buffer + square_height * num, 9, square_height - 1, lt=0, fill=color)
        # for num2, j in enumerate(go_list):
        #     if j in gene_go[i]:
        #         color = (0, 0, 200)
        #     else:
        #         color = (220, 220, 220)
        #     svg.drawOutRect(grid_start + 35 + square_width * len(rna_diff_dict[i]) + num2 * square_width, top_buffer + square_height * num, 9, 9, lt=0, fill=color)
        # color = (220, 220, 220)
        # for j in gene_go[i]:
        #     if not j in go_list:
        #         color = (0, 0, 200)
        #         break
        # svg.drawOutRect(grid_start + 35 + square_width * len(rna_diff_dict[i]) + len(go_list) * square_width, top_buffer + square_height * num, 9, 9, lt=0, fill=color)
    if diff_in_group:
        gene_groups.append(gene_group)

    last_loci = 'PROKKA_00000'
    opcolor = (100, 100, 200)
    diff_in_group = False
    grid_start = 700
    old_square_height = square_height
    square_height = 10
    square_width = 10
    gene_list = []
    count = 0
    old_top_buffer = top_buffer
    for i in gene_groups:
        y1 = top_buffer + i[0][1] * old_square_height
        y2 = top_buffer + count * square_height
        # svg.drawPath([400, 420, 600, grid_start], [y1, y1, y2, y2])
        for j in i:
            count += 1
            gene_list.append(j[0])
        y1 = top_buffer + i[-1][1] * old_square_height + old_square_height
        y2 = top_buffer + count * square_height
        # svg.drawPath([400, 420, 600, grid_start], [y1, y1, y2, y2])
    for num, i in enumerate(gene_list):
        if gene_dict[i][0] != 'none':
            gene_name = gene_dict[i][0]
        else:
            gene_name = i
        gene_desc = gene_dict[i][2]
        if int(last_loci.split('_')[1]) != int(i.split('_')[1]) - 1:
            switchit = True
            if not last_loci == 'PROKKA_00000' and dir_dict[last_loci] == dir_dict[i]:
                switchit = False
                for j in range(int(last_loci.split('_')[1]) + 1, int(i.split('_')[1])):
                    if 'PROKKA_' + str(j).zfill(5) in dir_dict and dir_dict['PROKKA_' + str(j).zfill(5)] == dir_dict[i]:
                        switchit = True
                        break
            if switchit:
                top_buffer += 5
                if opcolor == (0, 100, 0):
                    opcolor = (100, 0, 100)
                else:
                    opcolor = (0, 100, 0)
        svg.writeString(gene_name, grid_start - 10, top_buffer + num * square_height + 0.75 * square_height, 10, justify='right', color=opcolor)
        svg.writeString(gene_desc, grid_start + (len(rna_diff_dict[i]) + len(go_list) + 1) * square_width + 45, top_buffer + num * square_height + 0.75 * square_height, 10, color=opcolor)
        last_loci = i
        if i in diff_dict:
            if ';' in diff_dict[i]:
                color = var_color['mult']
                change_set.add('mult')
            elif diff_dict[i].startswith('upstream'):
                dist = int(diff_dict[i].split(',')[1])
                change_set.add('promoter')
                if dist < 1000:
                    color = var_color['promoter']
                else:
                    color = (220, 220, 220)
            else:
                try:
                    change_set.add(diff_dict[i])
                    color = var_color[diff_dict[i]]
                except:
                    print 'ding ding ding', diff_dict[i]
                    color = (255, 0, 0)
        else:
            color = (220, 220, 220)
        svg.drawOutRect(grid_start, top_buffer + square_height * num, 19, square_height - 1, lt=0, fill=color)
        for num2, j in enumerate(rna_diff_dict[i]):
            if j < 0:
                r = 1 - min([1, j / -3])
                color = hsl_to_rgb(0, 0.9, r/2 + 0.5)
            else:
                b = 1 - min([1, j / 3])
                color = hsl_to_rgb(250, 0.9, b/2 + 0.5)
            svg.drawOutRect(grid_start + 30 + num2 * square_width, top_buffer + square_height * num, square_width - 1, square_height - 1, lt=0, fill=color)
        for num2, j in enumerate(go_list):
            if j in gene_go[i]:
                color = (0, 0, 200)
            else:
                color = (220, 220, 220)
            svg.drawOutRect(grid_start + 35 + square_width * len(rna_diff_dict[i]) + num2 * square_width, top_buffer + square_height * num, square_width-1, square_height-1, lt=0, fill=color)
    go_descriptions['none'] = 'none'
    for num, i in enumerate(go_list):
        svg.writeString(i, grid_start + 35 + square_width * len(headers) + num * square_width, old_top_buffer - 10, 10, justify='right', rotate=-1)
        svg.writeString(go_descriptions[i], grid_start + 35 + square_width * len(headers) + num * square_width, len(gene_list) * square_height + 10 + top_buffer, 10, rotate=-1)
    # svg.writeString('other', grid_start + 35 + square_width * len(headers) + len(go_list) * square_width, top_buffer - 10, 10, justify='right', rotate=-1)
    # svg.writeString('other', grid_start + 35 + square_width * len(headers) + len(go_list) * square_width, len(gene_list) * square_height + 10 + top_buffer, 10, rotate=-1)
    if not panel3 is None:
        rna_diff_dict = {}
        rna_pval_dict ={}
        gene_list = []
        with open(panel3) as f:
            f.readline()
            for line in f:
                name, updown, c1, c2, c3, c4, p1, p2, p3, p4 = line.split()
                rna_diff_dict[name] = map(float, [c1, c2, c3, c4])
                rna_pval_dict[name] = [p1, p2, p3, p4]
                gene_list.append(name)
        gene_list.sort()
        last_loci = 'PROKKA_00000'
        opcolor = (100, 100, 200)
        diff_in_group = False
        grid_start = 2000
        square_height = 10
        square_width = 10
        count = 0
        old_top_buffer = top_buffer
        total_height = len(gene_list) * square_height
        for i in loc_lengths:
            length, chrom = i
            start = loc_starts[chrom]
            svg.drawOutRect(grid_start - 200, start * 1.0 / total_bp * total_height + top_buffer, 20, length * 1.0 / total_bp * total_height)
        print len(gene_list)
        for num, i in enumerate(gene_list):
            if gene_dict[i][0] != 'none':
                gene_name = gene_dict[i][0]
            else:
                gene_name = i
            gene_desc = gene_dict[i][2]
            if int(last_loci.split('_')[1]) != int(i.split('_')[1]) - 1:
                switchit = True
                if not last_loci == 'PROKKA_00000' and dir_dict[last_loci] == dir_dict[i]:
                    switchit = False
                    for j in range(int(last_loci.split('_')[1]) + 1, int(i.split('_')[1])):
                        if 'PROKKA_' + str(j).zfill(5) in dir_dict and dir_dict['PROKKA_' + str(j).zfill(5)] == dir_dict[i]:
                            switchit = True
                            break
                x1 = grid_start - 105
                if switchit:
                    x1 = grid_start - 100
                    if opcolor == (0, 100, 0):
                        opcolor = (100, 0, 100)
                    else:
                        opcolor = (0, 100, 0)
            y1 = loc_dict[i] * 1.0 / total_bp * total_height + top_buffer
            y2 = top_buffer + num * square_height + 0.3 * square_height
            svg.writeString(gene_name, grid_start - 10, top_buffer + num * square_height + 0.75 * square_height, 10, justify='right', color=opcolor)
            svg.writeString(gene_desc, grid_start + (len(rna_diff_dict[i]) + len(go_list) + 1 + len(rna_pval_dict[i])) * square_width + 45, top_buffer + num * square_height + 0.75 * square_height, 10, color=opcolor)
            svg.drawPath([grid_start - 200, grid_start - 180, grid_start -120, x1], [y1, y1, y2, y2], th=1, cl=opcolor)
            last_loci = i
            if i in diff_dict:
                if ';' in diff_dict[i]:
                    color = var_color['mult']
                    change_set.add('mult')
                elif diff_dict[i].startswith('upstream'):
                    dist = int(diff_dict[i].split(',')[1])
                    change_set.add('promoter')
                    if dist < 1000:
                        color = var_color['promoter']
                    else:
                        color = (220, 220, 220)
                else:
                    try:
                        change_set.add(diff_dict[i])
                        color = var_color[diff_dict[i]]
                    except:
                        print 'ding ding ding', diff_dict[i]
                        color = (255, 0, 0)
            else:
                color = (220, 220, 220)
            svg.drawOutRect(grid_start, top_buffer + square_height * num, 19, square_height - 1, lt=0, fill=color)
            for num2, j in enumerate(rna_diff_dict[i]):
                if j > 0:
                    r = 1 - min([1, j / 4])
                    color = hsl_to_rgb(0, 0.9, r/2 + 0.5)
                else:
                    b = 1 - min([1, j / -4])
                    color = hsl_to_rgb(250, 0.9, b/2 + 0.5)
                svg.drawOutRect(grid_start + 30 + num2 * square_width, top_buffer + square_height * num, square_width - 1, square_height - 1, lt=0, fill=color)
            for num2, j in enumerate(rna_pval_dict[i]):
                if j == '-4':
                    color = (255, 255, 255)
                if j == '-3':
                    color = (251,242,214)
                if j == '-2':
                    color  = (253,229,152)
                if j == '-1':
                    color = (253,192,15)
                svg.drawOutRect(grid_start + 30 + num2 * square_width + square_width * len(rna_diff_dict[i]), top_buffer + square_height * num, square_width - 1, square_height - 1, lt=0, fill=color)
            for num2, j in enumerate(go_list):
                if i in gene_go and j in gene_go[i]:
                    color = (0, 0, 200)
                else:
                    color = (220, 220, 220)
                svg.drawOutRect(grid_start + 35 + square_width * len(rna_diff_dict[i]) + square_width * len(rna_pval_dict[i]) + num2 * square_width, top_buffer + square_height * num, square_width-1, square_height-1, lt=0, fill=color)
        go_descriptions['none'] = 'none'
        for num, i in enumerate(go_list):
            svg.writeString(i, grid_start + 35 + square_width * len(headers) + num * square_width, old_top_buffer - 10, 10, justify='right', rotate=-1)
            svg.writeString(go_descriptions[i], grid_start + 35 + square_width * len(headers) + num * square_width, len(gene_list) * square_height + 10 + top_buffer, 10, rotate=-1)


    svg.writeString('Variant upstream ', grid_start - 10, top_buffer + (len(gene_list) + 5) * square_height + 0.75 * square_height, 10, justify='right')
    svg.writeString('Deletion in Blood', grid_start - 10, top_buffer + (len(gene_list) + 6) * square_height + 0.75 * square_height, 10, justify='right')
    svg.writeString('Partial deletion in blood', grid_start - 10, top_buffer + (len(gene_list) + 7) * square_height + 0.75 * square_height, 10, justify='right')
    svg.writeString('Nonsynonymous mutation in blood', grid_start - 10, top_buffer + (len(gene_list) + 8) * square_height + 0.75 * square_height, 10, justify='right')
    svg.writeString('Nonsynonymous mutation in nares', grid_start - 10, top_buffer + (len(gene_list) + 9) * square_height + 0.75 * square_height, 10, justify='right')
    svg.writeString('Synonymous mutation in blood', grid_start - 10, top_buffer + (len(gene_list) + 10) * square_height + 0.75 * square_height, 10, justify='right')
    svg.writeString('Plasmid loss', grid_start - 10, top_buffer + (len(gene_list) + 11) * square_height + 0.75 * square_height, 10, justify='right')
    svg.writeString('frameshift indel', grid_start - 10, top_buffer + (len(gene_list) + 12) * square_height + 0.75 * square_height, 10, justify='right')
    svg.writeString('More than one change', grid_start - 10, top_buffer + (len(gene_list) + 13) * square_height + 0.75 * square_height, 10, justify='right')

    svg.drawOutRect(grid_start, top_buffer + (len(gene_list) + 5) * square_height, 9, 9, lt=0, fill=var_color['promoter'])
    svg.drawOutRect(grid_start, top_buffer + (len(gene_list) + 6) * square_height, 9, 9, lt=0, fill=var_color['full_del'])
    svg.drawOutRect(grid_start, top_buffer + (len(gene_list) + 7) * square_height, 9, 9, lt=0, fill=var_color['partial_del'])
    svg.drawOutRect(grid_start, top_buffer + (len(gene_list) + 8) * square_height, 9, 9, lt=0, fill=var_color['nonsyn_query'])
    svg.drawOutRect(grid_start, top_buffer + (len(gene_list) + 9) * square_height, 9, 9, lt=0, fill=var_color['nonsyn_ref'])
    svg.drawOutRect(grid_start, top_buffer + (len(gene_list) + 10) * square_height, 9, 9, lt=0, fill=var_color['syn_query'])
    svg.drawOutRect(grid_start, top_buffer + (len(gene_list) + 11) * square_height, 9, 9, lt=0, fill=var_color['plasmid_loss'])
    svg.drawOutRect(grid_start, top_buffer + (len(gene_list) + 12) * square_height, 9, 9, lt=0, fill=var_color['deletion_query'])
    svg.drawOutRect(grid_start, top_buffer + (len(gene_list) + 13) * square_height, 9, 9, lt=0, fill=var_color['mult'])


    svg.writeString('Query upregulated 4x or greater logfold change', grid_start - 10, top_buffer + (len(gene_list) + 16) * square_height + 0.75 * square_height, 10, justify='right')
    svg.writeString('Query upregulated 3x logfold change', grid_start - 10, top_buffer + (len(gene_list) + 17) * square_height + 0.75 * square_height, 10, justify='right')
    svg.writeString('Query upregulated 2x logfold change', grid_start - 10, top_buffer + (len(gene_list) + 18) * square_height + 0.75 * square_height, 10, justify='right')
    svg.writeString('Query upregulated 1x logfold change', grid_start - 10, top_buffer + (len(gene_list) + 19) * square_height + 0.75 * square_height, 10, justify='right')
    svg.writeString('No change in regulation', grid_start - 10, top_buffer + (len(gene_list) + 20) * square_height + 0.75 * square_height, 10, justify='right')
    svg.writeString('Reference upregulated 1x logfold change', grid_start - 10, top_buffer + (len(gene_list) + 21) * square_height + 0.75 * square_height, 10, justify='right')
    svg.writeString('Reference upregulated 2x logfold change', grid_start - 10, top_buffer + (len(gene_list) + 22) * square_height + 0.75 * square_height, 10, justify='right')
    svg.writeString('Reference upregulated 3x logfold change', grid_start - 10, top_buffer + (len(gene_list) + 23) * square_height + 0.75 * square_height, 10, justify='right')
    svg.writeString('Reference upregulated 4x or greater logfold change', grid_start - 10, top_buffer + (len(gene_list) + 24) * square_height + 0.75 * square_height, 10, justify='right')


    svg.drawOutRect(grid_start, top_buffer + (len(gene_list) + 16) * square_height, 9, 9, lt=0, fill=hsl_to_rgb(0, 0.9, 0.5))
    svg.drawOutRect(grid_start, top_buffer + (len(gene_list) + 17) * square_height, 9, 9, lt=0, fill=hsl_to_rgb(0, 0.9, 0.625))
    svg.drawOutRect(grid_start, top_buffer + (len(gene_list) + 18) * square_height, 9, 9, lt=0, fill=hsl_to_rgb(0, 0.9, 0.75))
    svg.drawOutRect(grid_start, top_buffer + (len(gene_list) + 19) * square_height, 9, 9, lt=0, fill=hsl_to_rgb(0, 0.9, 0.875))
    svg.drawOutRect(grid_start, top_buffer + (len(gene_list) + 20) * square_height, 9, 9, lt=0, fill=hsl_to_rgb(0, 0.9, 1.0))
    svg.drawOutRect(grid_start, top_buffer + (len(gene_list) + 21) * square_height, 9, 9, lt=0, fill=hsl_to_rgb(250, 0.9, 0.875))
    svg.drawOutRect(grid_start, top_buffer + (len(gene_list) + 22) * square_height, 9, 9, lt=0, fill=hsl_to_rgb(250, 0.9, 0.75))
    svg.drawOutRect(grid_start, top_buffer + (len(gene_list) + 23) * square_height, 9, 9, lt=0, fill=hsl_to_rgb(250, 0.9, 0.625))
    svg.drawOutRect(grid_start, top_buffer + (len(gene_list) + 24) * square_height, 9, 9, lt=0, fill=hsl_to_rgb(250, 0.9, 0.5))
    svg.writesvg(out_file + '.svg')




add_change(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[8:], sys.argv[6], sys.argv[7])

