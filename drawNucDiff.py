import sys
import argparse
import subprocess
import os

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

    def drawLine(self, x1, y1, x2, y2, th=1, cl=(0, 0, 0), alpha = 1.0, linecap='round'):
        self.out += '  <line x1="%d" y1="%d" x2="%d" y2="%d"\n        stroke-width="%d" stroke="%s" stroke-opacity="%f" stroke-linecap="%s" />\n' % (x1, y1, x2, y2, th, colorstr(cl), alpha, linecap)

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



def translate_dna(dna):
    code = {     'ttt': 'F', 'tct': 'S', 'tat': 'Y', 'tgt': 'C',
         'ttc': 'F', 'tcc': 'S', 'tac': 'Y', 'tgc': 'C',
         'tta': 'L', 'tca': 'S', 'taa': '*', 'tga': '*',
         'ttg': 'L', 'tcg': 'S', 'tag': '*', 'tgg': 'W',
         'ctt': 'L', 'cct': 'P', 'cat': 'H', 'cgt': 'R',
         'ctc': 'L', 'ccc': 'P', 'cac': 'H', 'cgc': 'R',
         'cta': 'L', 'cca': 'P', 'caa': 'Q', 'cga': 'R',
         'ctg': 'L', 'ccg': 'P', 'cag': 'Q', 'cgg': 'R',
         'att': 'I', 'act': 'T', 'aat': 'N', 'agt': 'S',
         'atc': 'I', 'acc': 'T', 'aac': 'N', 'agc': 'S',
         'ata': 'I', 'aca': 'T', 'aaa': 'K', 'aga': 'R',
         'atg': 'M', 'acg': 'T', 'aag': 'K', 'agg': 'R',
         'gtt': 'V', 'gct': 'A', 'gat': 'D', 'ggt': 'G',
         'gtc': 'V', 'gcc': 'A', 'gac': 'D', 'ggc': 'G',
         'gta': 'V', 'gca': 'A', 'gaa': 'E', 'gga': 'G',
         'gtg': 'V', 'gcg': 'A', 'gag': 'E', 'ggg': 'G'
    }
    protein = ''
    dna = dna.lower()
    for i in range(0, len(dna), 3):
        if dna[i:i+3] in code:
            protein += code[dna[i:i+3]]
        else:
            protein += 'X'
    return protein

def reverse_compliment(seq):
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A', 'a': 't', 'c': 'g', 'g': 'c', 't': 'a'}
    return "".join(complement.get(base, base) for base in reversed(seq))

def read_nucdiff(in_path, query_genbank, ref_genbank, out_file, ref=False, merge=False, get_indel=False):
    if ref:
        next = '_ref_'
    else:
        next = '_query_'
    width = 50000
    x_margin = 2500
    y_margin = 2500
    y_gap = 1000
    line_height = 500
    line_space = 2500
    feature_height = 800
    feature_line_width = 100
    line_width = 20
    snv_line_width = 100
    genome_color = (100, 100, 100)
    genome_alpha = 0.5
    feature_alpha = 1
    label_gene = False
    text_size = 600
    if merge:
        height = y_margin * 2 + feature_height
    else:
        height = y_margin * 2 + feature_height * 4 + y_gap * 4
    svg = scalableVectorGraphics(height, width)
    color_list = [(240, 163, 255), (0, 117, 220), (153, 63, 0), (76, 0, 92), (25, 25, 25), (0, 92, 49), (43, 206, 72),
                  (255, 204, 153),
                  (128, 128, 128), (148, 255, 181), (143, 124, 0), (157, 204, 0), (194, 0, 136), (0, 51, 128),
                  (255, 164, 5), (255, 168, 187),
                  (66, 102, 0), (255, 0, 16), (94, 241, 242), (0, 153, 143), (224, 255, 102), (116, 10, 255),
                  (153, 0, 0), (255, 255, 128),
                  (255, 255, 0), (255, 80, 5), (0, 0, 0), (50, 50, 50)]

    colourDict = {
        'stop_gain': (240, 163, 255),
        'stop_loss': (0, 117, 220),
        'synonymous': (153, 63, 0),
        'nonsynonymous': (76, 0, 92),
        'intergenic': (255, 168, 187),
        'intergenic_insertion':(0, 92, 49),
        'intergenic_deletion':(43, 206, 72),
        'inframe_insertion':(255, 204, 153),
        'inframe_deletion':(194, 0, 136),
        'insertion': (148, 255, 181),
        'deletion': (143, 124, 0),
        'duplication': (157, 204, 0),
        'collapsed_repeat':(66, 102, 0),
        'substitution':(0, 51, 128),
        'inversion':(255, 164, 5),
        'collapsed_tandem_repeat':(255, 0, 16),
        'tandem_duplication':(94, 241, 242),
        'gap':(0, 153, 143),
        'translocation-overlap':(224, 255, 102),
        'relocation-overlap':(116, 10, 255),
        'relocation':(153, 0, 0)
    }
    query_names = set()
    with open(query_genbank) as gbk:
        gene_dict = {}
        getseq2 = False
        getseq = False
        seqDict = {}
        for line in gbk:
            if line.startswith('LOCUS'):
                contig_name = line.split()[1]
                query_names.add(contig_name)
                gene_dict[contig_name] = []
                genes = gene_dict[contig_name]
            elif line.startswith('     CDS             complement('):
                startstop = line.split('(')[1].split(')')[0]
                start, stop = map(int, startstop.split('..'))
                strand = '-'
                gene = 'none'
            elif line.startswith('     CDS '):
                startstop = line.split()[1]
                strand = '+'
                start, stop = map(int, startstop.split('..'))
                gene = 'none'
            elif line.startswith('                     /locus_tag'):
                locus_tag = line.split('"')[1]
            elif line.startswith('                     /gene='):
                gene = line.split('"')[1]
            elif line.startswith('                     /product='):
                product = line.split('"')[1]
            elif line.startswith('                     /translation='):
                seq = line.rstrip().split('"')[1]
                if line.count('"') == 2:
                    genes.append((start, stop, strand, gene, locus_tag, seq, product))
                else:
                    getseq = True
            elif getseq:
                seq += line.split()[0]
                if seq.endswith('"'):
                    genes.append((start, stop, strand, gene, locus_tag, seq[:-1], product))
                    getseq = False
            elif line.startswith('ORIGIN'):
                getseq2 = True
                seq = ''
            elif line.startswith('//'):
                seqDict[contig_name] = seq
                getseq2 = False
            elif getseq2:
                seq += ''.join(line.split()[1:])
    with open(ref_genbank) as gbk:
        getseq2 = False
        getseq = False
        for line in gbk:
            if line.startswith('LOCUS'):
                contig_name = line.split()[1]
                gene_dict[contig_name] = []
                genes = gene_dict[contig_name]
            elif line.startswith('     CDS             complement('):
                startstop = line.split('(')[1].split(')')[0]
                start, stop = map(int, startstop.split('..'))
                strand = '-'
                gene = 'none'
            elif line.startswith('     CDS '):
                startstop = line.split()[1]
                strand = '+'
                start, stop = map(int, startstop.split('..'))
                gene = 'none'
            elif line.startswith('                     /locus_tag'):
                locus_tag = line.split('"')[1]
            elif line.startswith('                     /gene='):
                gene = line.split('"')[1]
            elif line.startswith('                     /product='):
                product = line.split('"')[1]
            elif line.startswith('                     /translation='):
                seq = line.rstrip().split('"')[1]
                if line.count('"') == 2:
                    genes.append((start, stop, strand, gene, locus_tag, seq, product))
                else:
                    getseq = True
            elif getseq:
                seq += line.split()[0]
                if seq.endswith('"'):
                    genes.append((start, stop, strand, gene, locus_tag, seq[:-1], product))
                    getseq = False
            elif line.startswith('ORIGIN'):
                getseq2 = True
                seq = ''
            elif line.startswith('//'):
                seqDict[contig_name] = seq
                getseq2 = False
            elif getseq2:
                seq += ''.join(line.split()[1:])
    fig_width = width - x_margin * 2
    max_width = 3500000
    len_list = []
    for i in seqDict:
        len_list.append((len(seqDict[i]), i))
    len_list.sort(reverse=True)
    contig_gap = 800
    contig_offset = {}
    curr_x = x_margin
    for i in len_list:
        contig_offset[i[1]] = curr_x
        svg.drawLine(curr_x, y_margin + feature_height/2, curr_x + i[0] * 1.0 / max_width * (fig_width - (len(len_list) - 1) * contig_gap), y_margin + feature_height/2, line_height, genome_color, genome_alpha)
        curr_x += i[0] * 1.0 / max_width * (fig_width - (len(len_list) - 1) * contig_gap) + contig_gap
    snv_name_set, struct_name_set = set(), set()
    new_gff = open(out_file + '.gff', 'w')
    with open(in_path + next + 'snps.gff') as snps:
        for line in snps:
            if not line.startswith('#'):
                contig, program, so, query_start, query_stop, score, strand, phase, extra = line.rstrip().split('\t')
                if not contig in query_names:
                    print contig, query_names
                    sys.exit('You may have switched query and reference genbanks.')
                query_start = int(query_start)
                query_stop = int(query_stop)
                the_id, name, length, query_dir, ref_contig, ref_coord, query_bases, ref_bases, color = extra.split(';')
                name = name.split('=')[1]
                length = int(length.split('=')[1])
                ref_bases = ref_bases.split('=')[1]
                query_bases = query_bases.split('=')[1]
                if query_bases == '-':
                    query_bases = ''
                if ref_bases == '-':
                    ref_bases = ''
                gene_name = 'none'
                locus_tag = 'none'
                mut_type = 'intergenic'
                for i in gene_dict[contig]:
                    start, stop, strand, gene, locus, seq, product = i
                    if start <= query_start <= stop or start <= query_stop <= stop:
                        gene_seq = seqDict[contig][start-1:stop]
                        gene_seq_altered = seqDict[contig][start-1:query_start-1] + ref_bases + seqDict[contig][query_stop:stop]
                        gene_name = gene
                        locus_tag = locus
                        if strand == '-':
                            gene_seq = reverse_compliment(gene_seq)
                            gene_seq_altered = reverse_compliment(gene_seq_altered)
                        aa_seq = translate_dna(gene_seq)
                        aa_seq_altered = translate_dna(gene_seq_altered)
                        if not '*' in aa_seq_altered:
                            mut_type = 'stop_gain'
                        elif '*' in aa_seq_altered[:-1]:
                            mut_type = 'stop_loss'
                        elif aa_seq == aa_seq_altered:
                            mut_type = 'synonymous'
                        else:
                            mut_type = 'nonsynonymous'
                        break
                if name == 'substitution':
                    name = mut_type
                elif name == 'insertion':
                    if mut_type == 'intergenic':
                        name = 'intergenic_insertion'
                    elif (len(ref_bases) - len(query_bases)) % 3 == 0:
                        name = 'inframe_insertion'
                elif name == 'deletion':
                    if mut_type == 'intergenic':
                        name = 'intergenic_deletion'
                    elif (len(ref_bases) - len(query_bases)) % 3 == 0:
                        name = 'inframe_deletion'
                # len(seqDict[contig])
                if (not 'insertion' in name and not 'deletion' in name) or get_indel:
                    # sys.stdout.write(name + '\t' + gene + '\t' + locus + '\t' + product + '\n')
                    new_gff.write(line.rstrip() + ';mut_type=' + name + ';gene=' + gene_name + ',' + locus_tag + '\n')
                    x = int(query_start * 1.0 / max_width * fig_width) + contig_offset[contig]
                    svg.drawLine(x, y_margin, x, y_margin + feature_height, snv_line_width, colourDict[name])
                    snv_name_set.add(name)
                    if label_gene:
                        svg.writeString(gene, x + text_size/4, y_margin, text_size, rotate=1)
    with open(in_path + next + 'struct.gff') as struct:
        # y_margin += line_space
        shuffle_list = []
        to_draw = []
        for line in struct:
            if not line.startswith('#'):
                contig, program, so, query_start, query_stop, score, strand, phase, extra = line.rstrip().split('\t')
                query_start = int(query_start)
                query_stop = int(query_stop)
                name = extra.split(';')[1].split('=')[1]
                x = int(query_start * 1.0 / max_width * fig_width) + contig_offset[contig]
                ref_name = None
                ref_start = None
                ref_stop = None
                the_id = None
                name = None
                print 'dong'
                for i in extra.split(';'):
                    if i.startswith('ref_sequence=') or i.startswith('ref_sequence_1='):
                        ref_name = i.split('=')[1]
                        print 'ding'
                    elif i.startswith('ref_coord='):
                        if '-' in i.split('=')[1]:
                            ref_start, ref_stop = i.split('=')[1].split('-')
                        else:
                            ref_start = i.split('=')[1]
                            ref_stop = i.split('=')[1]
                        ref_start = int(ref_start)
                        ref_stop = int(ref_stop)
                    elif i.startswith('ID='):
                        the_id = i.split('=')[1]
                    elif i.startswith('ins_len='):
                        ins_length = i.split('=')[1]
                    elif i.startswith('Name'):
                        name = i.split('=')[1]
                    else:
                        print i
                struct_name_set.add(name)
                new_gff.write(line.rstrip())
                for i in gene_dict[contig]:
                    start, stop, strand, gene, locus, seq, product = i
                    if start <= query_start <= query_stop <= stop:
                        new_gff.write(';in_gene=' + gene + ',' + locus)
                    elif query_start <= start <= stop <= query_stop:
                        if not name in ['inversion'] or query_stop - query_start < 20000:
                            new_gff.write(';contains_gene=' + gene + ',' + locus)
                    elif start <= query_start <= stop or start <= query_stop <= stop:
                        new_gff.write(';partial_overlap=' + gene + ',' + locus)
                for i in gene_dict[ref_name]:
                    start, stop, strand, gene, locus, seq, product = i
                    if start <= ref_start <= ref_stop <= stop:
                        new_gff.write(';ref_in_gene=' + gene + ',' + locus)
                    elif ref_start <= start <= stop <= ref_stop:
                        if not name in ['inversion'] or query_stop - query_start < 20000:
                             new_gff.write(';ref_contains_gene=' + gene + ',' + locus)
                    elif start <= ref_start <= stop or start <= ref_stop <= stop:
                        new_gff.write(';ref_partial_overlap=' + gene + ',' + locus)
                    new_gff.write('\n')
                if name.startswith('reshuffling'):
                    the_id, the_name, length, query_dir, ref_contig, ref_coord, color = extra.split(';')
                    shuffle_num = int(the_name.split('_')[1])
                    shuffle_list.append((shuffle_num, query_start, query_stop))
                elif name == 'translocation-overlap' or name == 'relocation-overlap' or name == 'relocation':
                    # print extra.split(';')
                    # the_id, the_name, length, ref_contig, query_coord_1, ref_coord_1, query_len_1, ref_len_1, query_start_1,\
                    # ref_start_1, query_end_1, ref_end_1,  query_coord_2, ref_coord_2, query_len_2, ref_len_2,\
                    # query_start_2, ref_start_2, query_end_2, ref_end_2, color = extra.split(';')
                    width = int((query_stop - query_start) * 1.0 / max_width * fig_width)
                    if width <= feature_line_width:
                        feature_alpha1 = 0
                    else:
                        feature_alpha1 = feature_alpha
                    to_draw.append((x, y_margin, width, feature_height, colourDict[name], colourDict[name], feature_line_width, feature_alpha, feature_alpha1))
                elif name in ['insertion', 'substitution', 'inversion']:
                    the_id, the_name, length, query_dir, ref_contig, ref_coord, color = extra.split(';')
                    width = int((query_stop - query_start) * 1.0 / max_width * fig_width)
                    if width == 0: width = 1
                    if width <= feature_line_width:
                        feature_alpha1 = 0
                    else:
                        feature_alpha1 = feature_alpha
                    to_draw.append((x, y_margin, width, feature_height, colourDict[name], colourDict[name], feature_line_width, feature_alpha, feature_alpha1))
                elif name == 'deletion':
                    the_id, the_name, length, query_dir, ref_contig, ref_coord, color = extra.split(';')
                    width = int(length.split('=')[1])
                    width = int(width * 1.0 / max_width * fig_width)
                    if width == 0: width = 1
                    if width <= feature_line_width:
                        feature_alpha1 = 0
                    else:
                        feature_alpha1 = feature_alpha
                    svg.drawLine(x+width*1.0/2, y_margin - feature_height * 1.5 + feature_height, x+width*1.0/2, y_margin + feature_height, line_width, (0, 0, 0), feature_alpha, 'butt')
                    to_draw.append((x, y_margin - feature_height * 1.5, width, feature_height, colourDict[name], colourDict[name], feature_line_width, feature_alpha, feature_alpha1))
                elif name == 'duplication':
                    if len(extra.split(';')) == 8:
                        the_id, the_name, length, query_dir, ref_contig, ref_coord, repeat_coord, color = extra.split(';')
                    else:
                        the_id, the_name, length, query_dir, ref_contig, ref_coord, color = extra.split(';')
                    width = int((query_stop - query_start) * 1.0 / max_width * fig_width)
                    #
                    # rep_x = int(repeat_coord.split('=')[1].split('-')[0])
                    # rep_x = int(rep_x * 1.0 / max_width * fig_width) + contig_offset[contig]
                    if width == 0: width = 1
                    if width <= feature_line_width:
                        feature_alpha1 = 0
                    else:
                        feature_alpha1 = feature_alpha
                    to_draw.append((x, y_margin, width, feature_height, colourDict[name], colourDict[name], feature_line_width, feature_alpha, feature_alpha1))
                    # to_draw.append((rep_x, y_margin, width, feature_height, colourDict[name], colourDict[name], feature_line_width, feature_alpha, feature_alpha1))

                    # svg.drawPath([x + width/2, (x+rep_x)/2, rep_x+width/2], [y_margin, y_margin -feature_height/2, y_margin], line_width, (0, 0, 0), feature_alpha)
                elif name == 'collapsed_repeat':
                    if len(extra.split(';')) == 8:
                        the_id, the_name, length, query_dir, ref_contig, ref_coord, repeat_coord, color = extra.split(';')
                    else:
                        the_id, the_name, length, query_dir, ref_contig, ref_coord, color = extra.split(';')
                        repeat_coord = 'none'


                    width = int((query_stop - query_start) * 1.0 / max_width * fig_width)
                    # rep_x = int(repeat_coord.split('=')[1].split('-')[0])
                    # rep_x = int(rep_x * 1.0 / max_width * fig_width) + contig_offset[contig]
                    if width == 0: width = 1
                    if width <= feature_line_width:
                        feature_alpha1 = 0
                    else:
                        feature_alpha1 = feature_alpha
                    to_draw.append((x, y_margin, width, feature_height, colourDict[name], colourDict[name],
                                    feature_line_width, feature_alpha, feature_alpha1))
                elif name == 'tandem_duplication' or name == 'collapsed_tandem_repeat':
                    # the_id, the_name, length, query_dir, ref_contig, ref_coord, repeat_coord, repeat_coord2, color = extra.split(';')
                    width = int((query_stop - query_start) * 1.0 / max_width * fig_width)
                    if width == 0: width = 1
                    if width <= feature_line_width:
                        feature_alpha1 = 0
                    else:
                        feature_alpha1 = feature_alpha
                    to_draw.append((x, y_margin, width, feature_height, colourDict[name], colourDict[name],
                                    feature_line_width, feature_alpha, feature_alpha1))
                elif name == 'unaligned_end' or name == 'unaligned_beginning':
                    sys.stderr.write('Warning, contigs have unaligned ends - ensure they are orientated correctly\n')
                else:
                    sys.stderr.write(name + ' could not be interperated by this script\n')
                    # sys.exit()
        to_draw.sort(key=lambda x:x[2])
        for i in to_draw:
            a, b, c, d, e, f, g, h, i = i
            svg.drawOutRect(a, b, c, d, e, f, g, h, i)
        shuffle_list.sort(key=lambda x:x[1] -x[2])
        y_margin += y_gap
        for i in shuffle_list:
            pos, start, stop = i
            h = int(pos * 1.0 / len(shuffle_list) * 360)
            x1 = int(start * 1.0 / max_width * fig_width) + x_margin
            x2 = int(stop * 1.0 / max_width * fig_width) + x_margin
            if x2 == x1:
                x2 += 1
            x_margin, y_margin + feature_height / 2, fig_width, y_margin + feature_height / 2, line_height, genome_color, genome_alpha
            color = hsl_to_rgb(h, 0.5, 0.5)
            # svg.drawLine(x1, y_margin + feature_height / 2, x2, y_margin + feature_height / 2, line_height, color, genome_alpha, 'butt')
    curr_y = y_margin + y_gap
    for i in snv_name_set:
        svg.drawLine(x_margin, curr_y, x_margin, curr_y + feature_height, snv_line_width, colourDict[i])
        svg.writeString(i.replace('_', ' '), x_margin + feature_height*3/4, curr_y + feature_height * 3 / 4, text_size)
        curr_y += feature_height + 200
    # for i in struct_name_set:
    #     svg.drawOutRect(x_margin, curr_y, feature_height/2, feature_height, colourDict[i], colourDict[i], feature_line_width, feature_alpha, feature_alpha)
    #     svg.writeString(i.replace('_', ' '), x_margin + feature_height*3/4, curr_y + feature_height * 3 / 4, text_size)
    #     curr_y += feature_height + 200




    # with open(in_path + next + 'snps.gff'):
    # with open(in_path + next + 'snps.gff'):
    svg.writesvg(out_file + '.svg')


def gbk_to_fasta(gbk, out, concat=True):
    getseq = False
    if concat:
        with open(gbk) as f, open(out, 'w') as o:
            for line in f:
                if line.startswith('LOCUS'):
                    name = line.split()[1]
                    o.write('>' + name + '\n')
                elif line.startswith('ORIGIN'):
                    getseq = True
                elif line.startswith('//'):
                    getseq = False
                elif getseq:
                    o.write(''.join(line.split()[1:]) + '\n')
    else:
        with open(gbk) as f:
            for line in f:
                if line.startswith('LOCUS'):
                    name = line.split()[1]
                    o = open(out + '.' + name + '.fa', 'w')
                    o.write('>' + name + '\n')
                elif line.startswith('ORIGIN'):
                    getseq = True
                elif line.startswith('//'):
                    getseq = False
                    o.close()
                elif getseq:
                    o.write(''.join(line.split()[1:]) + '\n')


def get_contig_matches(query_gbk, ref_gbk, working_dir):
    gbk_to_fasta(query_gbk, working_dir + '/query_all.fa')
    gbk_to_fasta(ref_gbk, working_dir + '/ref_all.fa')
    subprocess.Popen('nucmer ' + working_dir + '/query_all.fa ' + working_dir + '/ref_all.fa --prefix ' + working_dir + '/all_v_all', shell=True).wait()
    subprocess.Popen('show-coords ' + working_dir + '/all_v_all.delta > ' + working_dir + '/all_v_all.coords', shell=True).wait()
    get_aligns = False
    best_match_query = {}
    best_match_ref = {}
    with open(working_dir + '/all_v_all.coords') as f:
        for line in f:
            if line.startswith('=================='):
                get_aligns = True
            elif get_aligns:
                s1, e1, bar, s2, e2, bar, l1, l2, bar, idy, bar, query, ref = line.split()
                if not query in best_match_query or int(l1) > best_match_query[query][0]:
                    best_match_query[query] = (int(l1), ref)
                if not ref in best_match_ref or int(l1) > best_match_ref[ref][0]:
                    best_match_ref[ref] = (int(l1), query)
    print best_match_query
    print best_match_ref
    pairs = []
    gbk_to_fasta(query_gbk, working_dir + '/' + os.path.splitext(os.path.basename(query_gbk))[0], False)
    gbk_to_fasta(ref_gbk, working_dir + '/' + os.path.splitext(os.path.basename(ref_gbk))[0], False)
    for i in best_match_query:
        if best_match_ref[best_match_query[i][1]][1] == i:
            pairs.append((i, best_match_query[i][1]))
    for i in pairs:
        subprocess.Popen(nucdiff_path)



parser = argparse.ArgumentParser()
parser.add_argument("-o", "--output", help="Will create an svg and gff of changes")
parser.add_argument("-qg", "--query_genbank", help="Concatenated genbank of genome", metavar="genome.gbk")
parser.add_argument("-rg", "--ref_genbank", help="Concatenated genbank of genome", metavar="genome.gbk")
parser.add_argument("-f", '--folder', help="nucdiff folder")
parser.add_argument("-w", '--working_dir', help="Add distance values")
parser.add_argument("-r", '--reference', action="store_true", default=False, help="Look at changes to reference not query")
args = parser.parse_args()

if not os.path.exists(args.working_dir):
    os.makedirs(args.working_dir)

get_contig_matches(args.query_genbank, args.ref_genbank, args.working_dir)
sys.exit()

read_nucdiff(infile, args.query_genbank, args.ref_genbank, args.output, args.reference)