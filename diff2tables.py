import sys
import os
import subprocess
import urllib2
import seaborn as sns
import numpy
import pandas
import math
from decimal import Decimal
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import FloatVector


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




def get_loci_group(locus, gen_folder, r_name, refs, homolog):
    min_ident = 90
    min_length = 0.90
    description = 'Hypothetical protein'
    inference = 'none'
    with open(gen_folder + '/' + r_name + '.gbk') as gbk:
        get_seq = 0
        for line in gbk:
            if line.startswith('                     /locus_tag="' + locus):
                get_seq = 1
            elif line.startswith('                     /inference="similar to AA sequence') and get_seq == 1:
                inference = line.split('"')[1].split(':')[-1]
            elif line.startswith('                     /inference="protein motif:Pfam:') and get_seq == 1:
                inference = line.split(':')[-1].split('.')[0]
            elif line.startswith('                     /product="') and get_seq == 1:
                description = line.split('"')[1]
            elif line.startswith('                     /translation="') and get_seq == 1:
                the_seq = line.split()[0]
                get_seq = 2
            elif get_seq == 2:
                the_seq += line.split()[0]
                if the_seq[-1] == '"':
                    break
    the_name = r_name + '.' + locus
    the_seq = the_seq.split('"')[1]
    query = open('tempquery.fa', 'w')
    query.write('>' + the_name + '\n' + the_seq)
    query.close()
    reference = open('tempref.fa', 'w')
    if refs != []:
        length_dict = {}
        for j in refs:
            reference.write('>' + j[0] + '\n' + j[1] + '\n')
            length_dict[j[0]] = len(j[1])
        reference.close()
        subprocess.Popen('makeblastdb -dbtype prot -in tempref.fa -out tempdb', shell=True, stdout=subprocess.PIPE).wait()
        subprocess.Popen('blastp -db tempdb -query tempquery.fa -outfmt 6 -out tempblast', shell=True).wait()
        found_one = False
        with open('tempblast') as blast:
            for line in blast:
                query, subject, ident, length = line.split()[:4]
                if float(ident) >= min_ident and int(length) >= min_length * len(the_seq) and int(length) >= min_length * int(length_dict[subject]):
                    gene = subject
                    found_one = True
                    homolog[gene].append(the_name)
                    break
        if not found_one:
            gene = the_name
            homolog[gene] = []
            refs.append((the_name, the_seq, inference, description))
    else:
        gene = the_name
        refs.append((the_name, the_seq, inference, description))
    return gene, refs


def add_to_dict(the_name, the_gene, mut_type, the_dict):
    if the_name in the_dict:
        if the_gene in the_dict[the_name]:
            if not mut_type in the_dict[the_name][the_gene].split(','):
                the_dict[the_name][the_gene] += ',' + mut_type
        else:
            the_dict[the_name][the_gene] = mut_type
    else:
        the_dict[the_name] = {the_gene:mut_type}
    return the_dict


def get_adjacent_genes(gene, gen_folder, i):
    the_dir = None
    out_list = []
    prev_gene = None
    prev_gene_for = None
    prev_gene_rev = None
    with open(gen_folder + '/' + i + '.gbk') as gbk:
        for line in gbk:
            if line.startswith('     CDS'):
                if 'complement' in line:
                    dir = False
                else:
                    dir = True
                gene_name = None
            elif line.startswith('                     /gene="'):
                gene_name = line.split('"')[1].split('_')[0]
            elif line.startswith('                     /locus_tag="'):
                if gene_name is None:
                    gene_name = i + '.' + line.split('"')[1]
            elif line.startswith('                     /translation="'):
                if dir == the_dir:
                    out_list.append(prev_gene)
                    out_list.append(gene_name)
                    the_dir = None
                if gene_name == gene:
                    the_dir = dir
                    if dir:
                        prev_gene= prev_gene_for
                    else:
                        prev_gene = prev_gene_rev
                if dir:
                    prev_gene_for = gene_name
                else:
                    prev_gene_rev = gene_name
    return out_list



def get_genes(folder, gen_folder, out_label, only_bio_process=False, do_go_enrich=False, only_snvs=True):
    out_dict = {}
    refs = []
    min_length = 0.90
    min_ident = 90
    ref_list = []
    table2 = open(out_label + '.table2.tsv', 'w')
    sorted_files = os.listdir(folder)
    sorted_files.sort()
    homolog = {}
    count_dict = {}
    count_var_set = set()
    reference_set = set()
    sv_groups = []
    plasmid_groups = []
    for diffs in sorted_files:
        if diffs.endswith('N_diff'):
            with open(folder + '/' + diffs) as diff_file:
                diff_file.readline()
                for line in diff_file:

                    gene_group = []
                    type, q_name, pos1, pos2, r_name, pos3, pos4, b1, b2, anc_type, mut_type, genes1, genes2, genes3, genes4, genes5, genes6, genes7, genes8, genes9, genes10 = line.split('\t')
                    reference_set.add(r_name)
                    count_var_set.add(mut_type)
                    if q_name in count_dict:
                        if mut_type in count_dict[q_name]:
                            count_dict[q_name][mut_type] += 1
                        else:
                            count_dict[q_name][mut_type] = 1
                    else:
                        count_dict[q_name] = {mut_type:1}
                    if not q_name in out_dict:
                        out_dict[q_name] = {}
                    if mut_type == 'nonsyn_query':
                        genes = genes1.split(';')
                        genes = filter(lambda a: a != 'none', genes)
                        for i in genes:
                            gene_name = i.split(',')[0].split('_')[0]
                            if gene_name == 'none':
                                gene_name, ref_list = get_loci_group(i.split(',')[1], gen_folder, q_name, ref_list, homolog)
                                if gene_name == q_name + '.' + i.split(',')[1]:
                                    homolog[gene_name] = []
                                else:
                                    homolog[gene_name].append(q_name + '.' + i.split(',')[1])
                            gene_group.append(gene_name)
                            out_dict = add_to_dict(q_name, gene_name, mut_type, out_dict)
                    elif mut_type == 'nonsyn_query_stop':
                        genes = genes1.split(';')
                        genes = filter(lambda a: a != 'none', genes)
                        for i in genes:
                            gene_name = i.split(',')[0].split('_')[0]
                            if gene_name == 'none':
                                gene_name, ref_list = get_loci_group(i.split(',')[1], gen_folder, q_name, ref_list, homolog)
                            gene_group.append(gene_name)
                            out_dict = add_to_dict(q_name, gene_name, mut_type, out_dict)
                    elif mut_type == 'syn_query':
                        genes = genes1.split(';')
                        genes = filter(lambda a: a != 'none', genes)
                        for i in genes:
                            gene_name = i.split(',')[0].split('_')[0]
                            if gene_name == 'none':
                                gene_name, ref_list = get_loci_group(i.split(',')[1], gen_folder, q_name, ref_list, homolog)
                            gene_group.append(gene_name)
                            out_dict = add_to_dict(q_name, gene_name, mut_type, out_dict)
                    elif mut_type == 'inframe_del_query':
                        genes = genes1.split(';')
                        genes = filter(lambda a: a != 'none', genes)
                        for i in genes:
                            gene_name = i.split(',')[0].split('_')[0]
                            if gene_name == 'none':
                                gene_name, ref_list = get_loci_group(i.split(',')[1], gen_folder, q_name, ref_list, homolog)
                            gene_group.append(gene_name)
                            out_dict = add_to_dict(q_name, gene_name, mut_type, out_dict)
                    elif mut_type == 'deletion_query':
                        genes = genes1.split(';')
                        genes = filter(lambda a: a != 'none', genes)
                        for i in genes:
                            gene_name = i.split(',')[0].split('_')[0]
                            if gene_name == 'none':
                                gene_name, ref_list = get_loci_group(i.split(',')[1], gen_folder, q_name, ref_list, homolog)
                            gene_group.append(gene_name)
                            out_dict = add_to_dict(q_name, gene_name, mut_type, out_dict)
                    elif mut_type == 'inframe_ins_query':
                        genes = genes1.split(';')
                        genes = filter(lambda a: a != 'none', genes)
                        for i in genes:
                            gene_name = i.split(',')[0].split('_')[0]
                            if gene_name == 'none':
                                gene_name, ref_list = get_loci_group(i.split(',')[1], gen_folder, q_name, ref_list, homolog)
                            gene_group.append(gene_name)
                            out_dict = add_to_dict(q_name, gene_name, mut_type, out_dict)
                    elif mut_type == 'insertion_query':
                        genes = genes1.split(';')
                        genes = filter(lambda a: a != 'none', genes)
                        for i in genes:
                            gene_name = i.split(',')[0].split('_')[0]
                            if gene_name == 'none':
                                gene_name, ref_list = get_loci_group(i.split(',')[1], gen_folder, q_name, ref_list, homolog)
                            gene_group.append(gene_name)
                            out_dict = add_to_dict(q_name, gene_name, mut_type, out_dict)
                    elif mut_type == 'syn_amb':
                        genes = genes1.split(';')
                        genes = filter(lambda a: a != 'none', genes)
                        for i in genes:
                            gene_name = i.split(',')[0].split('_')[0]
                            if gene_name == 'none':
                                gene_name, ref_list = get_loci_group(i.split(',')[1], gen_folder, q_name, ref_list, homolog)
                            gene_group.append(gene_name)
                            out_dict = add_to_dict(q_name, gene_name, mut_type, out_dict)
                    elif mut_type == 'syn_ref':
                        genes = genes1.split(';')
                        genes = filter(lambda a: a != 'none', genes)
                        for i in genes:
                            gene_name = i.split(',')[0].split('_')[0]
                            if gene_name == 'none':
                                gene_name, ref_list = get_loci_group(i.split(',')[1], gen_folder, q_name, ref_list, homolog)
                            gene_group.append(gene_name)
                            out_dict = add_to_dict(q_name, gene_name, mut_type, out_dict)
                    elif mut_type == 'nonsyn_amb':
                        genes = genes1.split(';')
                        genes = filter(lambda a: a != 'none', genes)
                        for i in genes:
                            gene_name = i.split(',')[0].split('_')[0]
                            if gene_name == 'none':
                                gene_name, ref_list = get_loci_group(i.split(',')[1], gen_folder, q_name, ref_list, homolog)
                            gene_group.append(gene_name)
                            out_dict = add_to_dict(q_name, gene_name, mut_type, out_dict)
                    elif mut_type == 'nonsyn_ref_stop':
                        genes = genes1.split(';')
                        genes = filter(lambda a: a != 'none', genes)
                        for i in genes:
                            gene_name = i.split(',')[0].split('_')[0]
                            if gene_name == 'none':
                                gene_name, ref_list = get_loci_group(i.split(',')[1], gen_folder, q_name, ref_list, homolog)
                            gene_group.append(gene_name)
                            out_dict = add_to_dict(q_name, gene_name, mut_type, out_dict)
                    elif mut_type == 'nonsyn_ref':
                        genes = genes1.split(';')
                        genes = filter(lambda a: a != 'none', genes)
                        for i in genes:
                            gene_name = i.split(',')[0].split('_')[0]
                            if gene_name == 'none':
                                gene_name, ref_list = get_loci_group(i.split(',')[1], gen_folder, q_name, ref_list, homolog)
                            gene_group.append(gene_name)
                            out_dict = add_to_dict(q_name, gene_name, mut_type, out_dict)
                    elif mut_type == 'intergenic_ref':
                        pass
                    elif mut_type == 'intergenic_query':
                        pass
                    elif mut_type == 'intergenic_amb':
                        pass
                    elif mut_type == 'no_matching_genes':
                        pass
                    elif mut_type == 'deletion in query' or mut_type == 'plasmid_loss':
                        genes = genes2.split(';') + genes4.split(';')
                        genes = filter(lambda a: a != 'none', genes)
                        the_length = b2
                        the_pos = pos1
                        table2.write('\t'.join([q_name, 'deletion', the_length, the_pos]))
                        first_gene = True
                        for i in genes:
                            gene_name = i.split(',')[0].split('_')[0]
                            if gene_name == 'none':
                                gene_name, ref_list = get_loci_group(i.split(',')[1], gen_folder, r_name, ref_list, homolog)
                                table_name = 'hypothetical protein'
                            else:
                                table_name = gene_name
                            if first_gene:
                                table2.write('\t' + table_name + '\t' + i.split(',')[1] + '\tgene partially deleted\n')
                                first_gene = False
                            else:
                                table2.write('\t\t\t\t' + table_name + '\t' + i.split(',')[1] + '\tgene partially deleted\n')
                            gene_group.append(gene_name)
                            out_dict = add_to_dict(q_name, gene_name, 'partial_del', out_dict)
                        genes = genes6.split(';')
                        genes = filter(lambda a: a != 'none', genes)
                        for i in genes:
                            gene_name = i.split(',')[0].split('_')[0]
                            if gene_name == 'none':
                                gene_name, ref_list = get_loci_group(i.split(',')[1], gen_folder, r_name, ref_list, homolog)
                                table_name = 'hypothetical protein'
                            else:
                                table_name = gene_name
                            if first_gene:
                                table2.write('\t' + table_name + '\t' + i.split(',')[1] + '\tgene deleted\n')
                                first_gene = False
                            else:
                                table2.write('\t\t\t\t' + table_name + '\t' + i.split(',')[1] + '\tgene deleted\n')
                            gene_group.append(gene_name)
                            out_dict = add_to_dict(q_name, gene_name, 'full_del', out_dict)
                        if first_gene:
                            table2.write('\tno genes affected\n')
                        if mut_type == 'deletion in query':
                            sv_groups.append(gene_group)
                        else:
                            plasmid_groups.append(gene_group)
                    elif mut_type == 'tandem contraction in query':
                        genes = genes1.split(';')
                        genes = filter(lambda a: a != 'none', genes)
                        the_length = str(abs(int(b2) - int(b1)))
                        the_pos = pos1
                        table2.write('\t'.join([q_name, 'tandem contraction', the_length, the_pos]))
                        first_gene = True
                        for i in genes:
                            gene_name = i.split(',')[0].split('_')[0]
                            if gene_name == 'none':
                                gene_name, ref_list = get_loci_group(i.split(',')[1], gen_folder, q_name, ref_list, homolog)
                                table_name = 'hypothetical protein'
                            else:
                                table_name = gene_name
                            if first_gene:
                                table2.write('\t' + table_name + '\t' + i.split(',')[1] + '\tcontraction in gene\n')
                                first_gene = False
                            else:
                                table2.write('\t\t\t\t' + table_name + '\t' + i.split(',')[1] + '\tcontraction in gene\n')
                            gene_group.append(gene_name)
                            out_dict = add_to_dict(q_name, gene_name, 'partial_del', out_dict)
                        if first_gene:
                            table2.write('\tno genes affected\n')
                        sv_groups.append(gene_group)
                    elif mut_type == 'deletion in query (duplicated ends)':
                        genes = genes2.split(';') + genes4.split(';')
                        genes = filter(lambda a: a != 'none', genes)
                        the_length = str(int(b2) + int(b1))
                        the_pos = pos1
                        table2.write('\t'.join([q_name, 'deletion (duplicated ends)', the_length, the_pos]))
                        first_gene = True
                        for i in genes:
                            gene_name = i.split(',')[0].split('_')[0]
                            if gene_name == 'none':
                                gene_name, ref_list = get_loci_group(i.split(',')[1], gen_folder, r_name, ref_list, homolog)
                                table_name = 'hypothetical protein'
                            else:
                                table_name = gene_name
                            if first_gene:
                                table2.write('\t' + table_name + '\t' + i.split(',')[1] + '\tgene partially deleted\n')
                                first_gene = False
                            else:
                                table2.write('\t\t\t\t' + table_name + '\t' + i.split(',')[1] + '\tgene partially deleted\n')
                            gene_group.append(gene_name)
                            out_dict = add_to_dict(q_name, gene_name, 'partial_del', out_dict)
                        genes = genes6.split(';')
                        genes = filter(lambda a: a != 'none', genes)
                        for i in genes:
                            gene_name = i.split(',')[0].split('_')[0]
                            if gene_name == 'none':
                                gene_name, ref_list = get_loci_group(i.split(',')[1], gen_folder, r_name, ref_list, homolog)
                                table_name = 'hypothetical protein'
                            else:
                                table_name = gene_name
                            if first_gene:
                                table2.write('\t' + table_name + '\t' + i.split(',')[1] + '\tgene deleted\n')
                                first_gene = False
                            else:
                                table2.write('\t\t\t\t' + table_name + '\t' + i.split(',')[1] + '\tgene deleted\n')
                            gene_group.append(gene_name)
                            out_dict = add_to_dict(q_name, gene_name, 'full_del', out_dict)
                        if first_gene:
                            table2.write('\tno genes affected\n')
                        sv_groups.append(gene_group)
                    elif mut_type == 'tandem expansion in query':
                        genes = genes1.split(';')
                        genes = filter(lambda a: a != 'none', genes)
                        the_length = str(abs(int(b2) - int(b1)))
                        the_pos = pos1
                        table2.write('\t'.join([q_name, 'tandem expansion', the_length, the_pos]))
                        first_gene = True
                        for i in genes:
                            gene_name = i.split(',')[0].split('_')[0]
                            if gene_name == 'none':
                                gene_name, ref_list = get_loci_group(i.split(',')[1], gen_folder, q_name, ref_list, homolog)
                                table_name = 'hypothetical protein'
                            else:
                                table_name = gene_name
                            if first_gene:
                                table2.write('\t' + table_name + '\t' + i.split(',')[1] + '\texpansion in gene\n')
                                first_gene = False
                            else:
                                table2.write('\t\t\t\t' + table_name + '\t' + i.split(',')[1] + '\texpansion in gene\n')
                            gene_group.append(gene_name)
                            out_dict = add_to_dict(q_name, gene_name, 'partial_ins', out_dict)
                        if first_gene:
                            table2.write('\tno genes affected\n')
                        sv_groups.append(gene_group)
                    elif mut_type == 'insertion in query' or mut_type == 'plasmid_gain':
                        genes = genes1.split(';') + genes3.split(';')
                        genes = filter(lambda a: a != 'none', genes)
                        the_length = b1
                        the_pos = pos1
                        table2.write('\t'.join([q_name, 'Insertion', the_length, the_pos]))
                        first_gene = True
                        for i in genes:
                            gene_name = i.split(',')[0].split('_')[0]
                            if gene_name == 'none':
                                gene_name, ref_list = get_loci_group(i.split(',')[1], gen_folder, q_name, ref_list, homolog)
                                table_name = 'hypothetical protein'
                            else:
                                table_name = gene_name
                            if first_gene:
                                table2.write('\t' + table_name + '\t' + i.split(',')[1] + '\tgene altered by insertion\n')
                                first_gene = False
                            else:
                                table2.write('\t\t\t\t' + table_name + '\t' + i.split(',')[1] + '\tgene altered by insertion\n')
                            gene_group.append(gene_name)
                            out_dict = add_to_dict(q_name, gene_name, 'partial_ins', out_dict)
                        genes = genes5.split(';')
                        genes = filter(lambda a: a != 'none', genes)
                        for i in genes:
                            gene_name = i.split(',')[0].split('_')[0]
                            if gene_name == 'none':
                                gene_name, ref_list = get_loci_group(i.split(',')[1], gen_folder, q_name, ref_list, homolog)
                                table_name = 'hypothetical protein'
                            else:
                                table_name = gene_name
                            if first_gene:
                                table2.write('\t' + table_name + '\t' + i.split(',')[1] + '\tgene inserted\n')
                                first_gene = False
                            else:
                                table2.write('\t\t\t\t' + table_name + '\t' + i.split(',')[1] + '\tgene inserted\n')
                            gene_group.append(gene_name)
                            out_dict = add_to_dict(q_name, gene_name, 'full_ins', out_dict)
                        if first_gene:
                            table2.write('\tno genes affected\n')
                        if mut_type == 'insertion in query':
                            sv_groups.append(gene_group)
                        else:
                            plasmid_groups.append(gene_group)
                    elif mut_type == 'insertion in query (duplicated ends)':
                        genes = genes1.split(';') + genes3.split(';')
                        genes = filter(lambda a: a != 'none', genes)
                        the_length = str(int(b1) + int(b2))
                        the_pos = pos1
                        table2.write('\t'.join([q_name, 'insertion (duplicated ends)', the_length, the_pos]))
                        first_gene = True
                        for i in genes:
                            gene_name = i.split(',')[0].split('_')[0]
                            if gene_name == 'none':
                                gene_name, ref_list = get_loci_group(i.split(',')[1], gen_folder, q_name, ref_list, homolog)
                                table_name = 'hypothetical protein'
                            else:
                                table_name = gene_name
                            if first_gene:
                                table2.write('\t' + table_name + '\t' + i.split(',')[1] + '\tgene altered by insertion\n')
                                first_gene = False
                            else:
                                table2.write('\t\t\t\t' + table_name + '\t' + i.split(',')[1] + '\tgene altered by insertion\n')
                            gene_group.append(gene_name)
                            out_dict = add_to_dict(q_name, gene_name, 'partial_ins', out_dict)
                        genes = genes5.split(';')
                        genes = filter(lambda a: a != 'none', genes)
                        for i in genes:
                            gene_name = i.split(',')[0].split('_')[0]
                            if gene_name == 'none':
                                gene_name, ref_list = get_loci_group(i.split(',')[1], gen_folder, q_name, ref_list, homolog)
                                table_name = 'hypothetical protein'
                            else:
                                table_name = gene_name
                            if first_gene:
                                table2.write('\t' + table_name + '\t' + i.split(',')[1] + '\tgene inserted\n')
                                first_gene = False
                            else:
                                table2.write('\t\t\t\t' + table_name + '\t' + i.split(',')[1] + '\tgene inserted\n')
                            gene_group.append(gene_name)
                            out_dict = add_to_dict(q_name, gene_name, 'full_ins', out_dict)
                        if first_gene:
                            table2.write('\tno genes affected\n')
                        sv_groups.append(gene_group)
                    elif mut_type == 'inversion':
                        genes = genes5.split(';')
                        genes = filter(lambda a: a != 'none', genes)
                        the_length = b1
                        the_pos = pos1
                        table2.write('\t'.join([q_name, 'Inversion', the_length, the_pos]))
                        first_gene = True
                        for i in genes:
                            gene_name = i.split(',')[0].split('_')[0]
                            if gene_name == 'none':
                                table_name = 'hypothetical protein'
                            else:
                                table_name = gene_name
                            if first_gene:
                                table2.write('\t' + table_name + '\t' + i.split(',')[1] + '\tgene inverted\n')
                                first_gene = False
                            else:
                                table2.write('\t\t\t\t' + table_name + '\t' + i.split(',')[1] + '\tgene inverted\n')
                        if first_gene:
                            table2.write('\tno genes affected\n')
                    elif mut_type == 'Variable region':
                        the_length = b1 + ',' + b2
                        the_pos = pos1
                        table2.write('\t'.join([q_name, 'Variable region', the_length, the_pos]))
                        first_gene = True
                        genes = genes6.split(';')
                        genes = filter(lambda a: a != 'none', genes)
                        for i in genes:
                            gene_name = i.split(',')[0].split('_')[0]
                            if gene_name == 'none':
                                gene_name, ref_list = get_loci_group(i.split(',')[1], gen_folder, r_name, ref_list, homolog)
                                table_name = 'hypothetical protein'
                            else:
                                table_name = gene_name
                            if first_gene:
                                table2.write('\t' + table_name + '\t' + i.split(',')[1] + '\tgene deleted\n')
                                first_gene = False
                            else:
                                table2.write('\t\t\t\t' + table_name + '\t' + i.split(',')[1] + '\tgene deleted\n')
                            gene_group.append(gene_name)
                            out_dict = add_to_dict(q_name, gene_name, 'full_del', out_dict)
                        genes = genes1.split(';') + genes3.split(';')
                        genes = filter(lambda a: a != 'none', genes)
                        for i in genes:
                            gene_name = i.split(',')[0].split('_')[0]
                            if gene_name == 'none':
                                gene_name, ref_list = get_loci_group(i.split(',')[1], gen_folder, q_name, ref_list, homolog)
                                table_name = 'hypothetical protein'
                            else:
                                table_name = gene_name
                            if first_gene:
                                table2.write('\t' + table_name + '\t' + i.split(',')[1] + '\tgene altered\n')
                                first_gene = False
                            else:
                                table2.write('\t\t\t\t' + table_name + '\t' + i.split(',')[1] + '\tgene altered\n')
                            gene_group.append(gene_name)
                            out_dict = add_to_dict(q_name, gene_name, 'partial_ins', out_dict)
                        genes = genes5.split(';')
                        genes = filter(lambda a: a != 'none', genes)
                        for i in genes:
                            gene_name = i.split(',')[0].split('_')[0]
                            if gene_name == 'none':
                                gene_name, ref_list = get_loci_group(i.split(',')[1], gen_folder, q_name, ref_list, homolog)
                                table_name = 'hypothetical protein'
                            else:
                                table_name = gene_name
                            if first_gene:
                                table2.write('\t' + table_name + '\t' + i.split(',')[1] + '\tinserted\n')
                                first_gene = False
                            else:
                                table2.write('\t\t\t\t' + table_name + '\t' + i.split(',')[1] + '\tinserted\n')
                            gene_group.append(gene_name)
                            out_dict = add_to_dict(q_name, gene_name, 'full_ins', out_dict)
                    else:
                        print mut_type, 'dong dong dong'
    table2.close()
    gene_list = set()
    description_dict = {}
    for i in out_dict:
        for j in out_dict[i]:
            gene_list.add(j)
    query = open('tempquery.fa', 'w')
    length_dict = {}
    for j in ref_list:
        query.write('>' + j[0] + '\n' + j[1] + '\n')
        length_dict[j[0]] = len(j[1])
        description_dict[j[0]] = (j[3], j[2])
    query.close()
    get_seq = False
    for i in out_dict:
        with open(gen_folder + '/' + i + '.gbk') as gbk:
            ref = open('tempref.fa', 'w')
            length_dict2 = {}
            for line in gbk:
                if line.startswith('     CDS'):
                    gene_name = None
                    description = 'Hypothetical protein'
                    inference = 'none'
                    get_seq = False
                elif line.startswith('                     /gene="'):
                    gene_name = line.split('"')[1].split('_')[0]
                    if gene_name in gene_list and not gene_name in out_dict[i]:
                        out_dict = add_to_dict(i, gene_name, 'present', out_dict)
                elif line.startswith('                     /locus_tag="'):
                    locus = line.split('"')[1]
                elif line.startswith('                     /inference="similar to AA sequence'):
                    inference = line.split('"')[1].split(':')[-1]
                elif line.startswith('                     /inference="protein motif:Pfam:'):
                    inference = line.split(':')[-1].split('.')[0]
                elif line.startswith('                     /product="'):
                    description = line.split('"')[1]
                elif line.startswith('                     /translation="') and line.rstrip().endswith('"'):
                    the_seq = line.split('"')[1]
                    ref.write('>' + locus + '\n' + the_seq + '\n')
                    length_dict2[locus] = len(the_seq)
                    if not gene_name is None:
                        description_dict[gene_name] = (description, inference)
                elif line.startswith('                     /translation="'):
                    the_seq = line.split()[0]
                    get_seq = True
                elif get_seq:
                    the_seq += line.split()[0]
                    if the_seq[-1] == '"':
                        get_seq = False
                        the_seq = the_seq.split('"')[1]
                        ref.write('>' + locus + '\n' + the_seq + '\n')
                        length_dict2[locus] = len(the_seq)
                        if not gene_name is None:
                            description_dict[gene_name] = (description, inference)
            ref.close()
        subprocess.Popen('makeblastdb -dbtype prot -in tempref.fa -out tempdb', shell=True, stdout=subprocess.PIPE).wait()
        subprocess.Popen('blastp -db tempdb -query tempquery.fa -outfmt 6 -out tempblast', shell=True).wait()
        with open('tempblast') as blast:
            for line in blast:
                query, subject, ident, length = line.split()[:4]
                if float(ident) >= min_ident and int(length) >= min_length * length_dict[query] and int(length) >= min_length * length_dict2[subject]:
                    if not query in out_dict[i]:
                        out_dict = add_to_dict(i, query, 'present', out_dict)
                        if query in homolog:
                            homolog[query].append(i + '.' + subject)
    for i in reference_set:
        with open(gen_folder + '/' + i + '.gbk') as gbk:
            for line in gbk:
                if line.startswith('     CDS'):
                    gene_name = None
                    description = 'Hypothetical protein'
                    inference = 'none'
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
                    if not gene_name is None:
                        description_dict[gene_name] = (description, inference)
    gene_list = list(gene_list)
    go_descriptions = {}
    gene_go = {}
    fam_acc = {}
    if not os.path.exists('this_is_a_go_file'):
        online_mode = True
        out_go = open('this_is_a_go_file', 'w')
    else:
        online_mode = False
        tiagd = {}
        with open('this_is_a_go_file') as tiagf:
            for line in tiagf:
                if line.split('\t')[0] in tiagd:
                    tiagd[line.split('\t')[0]].append(line.rstrip().split('\t')[1:])
                else:
                    tiagd[line.split('\t')[0]] = [line.rstrip().split('\t')[1:]]
    print 'using online mode', online_mode
    go_rel_dict = {}
    with open('go.obo') as goobo:
        for line in goobo:
            if line.startswith('id: '):
                go = line.rstrip()[4:]
                go_rel_dict[go] = []
            elif line.startswith('is_a: '):
                go_rel_dict[go].append(line.split()[1])
            elif line.startswith('relationship: part_of'):
                go_rel_dict[go].append(line.split()[2])
            elif line.startswith('name: '):
                go_descriptions[go] = line.rstrip()[6:]
    for i in description_dict:
        if description_dict[i][1].startswith('PF'):
            if description_dict[i][1] in fam_acc:
                fam_acc[description_dict[i][1]].append(i)
            else:
                fam_acc[description_dict[i][1]] = [i]
        elif description_dict[i][1] != 'none':
            if online_mode:
                req = urllib2.urlopen('http://www.ebi.ac.uk/QuickGO/GAnnotation?protein=' + description_dict[i][1] + '&format=tsv')
                print 'http://www.ebi.ac.uk/QuickGO/GAnnotation?protein=' + description_dict[i][1] + '&format=tsv'
                req.readline()
                for line in req:
                    go, desc = line.split('\t')[6:8]
                    out_go.write(description_dict[i][1] + '\t' + go + '\t' + desc + '\n')
                    if i in gene_go:
                        gene_go[i].add(go)
                    else:
                        gene_go[i] = set([go])
                    go_descriptions[go] = desc
                if not i in gene_go:

                    print i, 'http://www.uniprot.org/uniprot/' + description_dict[i][1] + '.rdf'
                    req = urllib2.urlopen('http://www.uniprot.org/uniprot/' + description_dict[i][1] + '.rdf')
                    new_accs = []
                    for line in req:
                        if line.startswith('<replacedBy rdf:resource='):
                            new_accs.append(line.split('"')[1].split('/')[-1])
                    print new_accs
                    if new_accs != []:
                        new_acc = new_accs[-1]
                        req = urllib2.urlopen('http://www.ebi.ac.uk/QuickGO/GAnnotation?protein=' + new_acc + '&format=tsv')
                        req.readline()
                        for line in req:
                            go, desc = line.split('\t')[6:8]
                            out_go.write(description_dict[i][1] + '\t' + go + '\t' + desc + '\n')
                            if i in gene_go:
                                gene_go[i].add(go)
                            else:
                                gene_go[i] = set([go])
                            go_descriptions[go] = desc
            else:
                if description_dict[i][1] in tiagd:
                    for j in tiagd[description_dict[i][1]]:
                        go, desc = j
                        if i in gene_go:
                            gene_go[i].add(go)
                        else:
                            gene_go[i] = set([go])
                        go_descriptions[go] = desc
    req = urllib2.urlopen('http://geneontology.org/external2go/pfam2go')
    for line in req:
        if not line.startswith('!'):
            if line.split()[0].split(':')[1] in fam_acc:
                genes = fam_acc[line.split()[0].split(':')[1]]
                go = line.split()[-1]
                desc = line.split(':')[2][:-5]
                go_descriptions[go] = desc
                for gene in genes:
                    if gene in gene_go:
                        gene_go[gene].add(go)
                    else:
                        gene_go[gene] = set([go])
    for i in gene_go:
        new_set = gene_go[i]
        old_set = set()
        while len(new_set) != len(old_set):
            old_set = new_set
            new_set = set()
            for j in old_set:
                new_set.add(j)
                try:
                    for k in go_rel_dict[j]:
                        new_set.add(k)
                except KeyError:
                    pass
        gene_go[i] = new_set
    go_list = set()
    new_gene_list = []
    phage_set = set()
    hypo_set = set()
    for i in gene_list:
        if description_dict[i][0] == 'hypothetical protein':
            hypo_set.add(i)
        elif 'phage' in description_dict[i][0] or 'Phage' in description_dict[i][0]:
            phage_set.add(i)
        else:
            getit = False
            for j in out_dict:
                if i in out_dict[j]:
                    for k in out_dict[j][i].split(','):
                        if not k.startswith('syn') and k != 'nonsyn_ref' and k != 'nonsyn_ref_stop' and k != 'present' and not only_snvs:
                            getit = True
                        elif (k == 'nonsyn_query' or k == 'nonsyn_query_stop' \
                                or k == 'inframe_del_query' or k == 'deletion_query' or k == 'inframe_ins_query' \
                                or k == 'insertion_query' or k == 'nonsyn_amb') and only_snvs:
                            getit = True
            if getit:
                new_gene_list.append(i)
    old_gene_list = gene_list
    gene_list = new_gene_list
    for i in gene_list:
        if i in gene_go:
            for j in gene_go[i]:
                go_list.add(j)
    go_list = list(go_list)
    if do_go_enrich:
        new_go_list = []
        pval_list = []
        for i in go_list:
            a, b, c, d = 0, 0, 0, 0
            for j in gene_go: # for all genes in pan genome
                if i in gene_go[j]: # if GO in gene
                    if j in gene_list: # if gene is mutated
                        a += 1
                    else: # if gene not mutated
                        c += 1
                else: # if go not in gene
                    if j in gene_list: # if gene mutated
                        b += 1
                    else: # if gene not mutated
                        d += 1
            print i, a, b, c, d
            pval = Decimal(math.factorial(a+b) * math.factorial(c+d) * math.factorial(a + c) * math.factorial(b + d)) / \
                   Decimal(math.factorial(a) * math.factorial(b) * math.factorial(c) * math.factorial(d) * math.factorial(a+b+c+d))
            pval_list.append(pval)
        stats = importr('stats')
        p_adjust = stats.p_adjust(FloatVector(pval_list), method = 'BY')
        for i in range(len(pval_list)):
            print pval_list[i], p_adjust[i]
        for num, i in enumerate(p_adjust):
            print go_list[num], pval_list[num], i
            if i <= 0.05:
                print 'ding'
                new_go_list.append(go_list[num])
        go_list = new_go_list
    go_list.sort()
    gene_list.sort()
    top_buffer = 400
    gene_name_start = 50
    grid_start = 400
    square_height = 10
    square_width = 10
    svg = scalableVectorGraphics(5000, 5000)
    test_out = open('test.out', 'w')

    new_go_list = []
    go_freq = {}
    go_gene_dict = {}
    for i in go_list: # create a list of genes in go category
        gene_set = set()
        for j in gene_list:
            if j in gene_go and i in gene_go[j]:
                gene_set.add(j)
        go_gene_dict[i] = gene_set
    go_groups = []
    # for each group of genes - get the lowest go heirachy for that group
    for i in go_gene_dict:
        gotit = False
        for j in go_groups:
            if j[1] == go_gene_dict[i]:
                j[0].append(i)
                gotit = True
                break
        if not gotit:
            go_groups.append([[i], go_gene_dict[i]])
    go_list = []
    for i in go_groups:
        parents = set()
        for j in i[0]:
            for k in go_rel_dict[j]:
                parents.add(k)
        for j in i[0]:
            if not j in parents:
                print j
                go_list.append(j)
    desc_set = set()
    for i in go_list:
        count = 0
        for j in gene_list:
            if j in gene_go and i in gene_go[j]:
                count += 1
        go_freq[i] = count
        if count > 5 and go_descriptions[i] not in desc_set:# and count < len(gene_list) * 0.2:
            new_go_list.append(i)
            go_freq[i] = count
            desc_set.add(go_descriptions[i])
    go_list = new_go_list
    if only_bio_process:
        new_go_list = []
        for i in go_descriptions: # find the biological process go term
            if go_descriptions[i] == 'biological_process':
                parent_go = i
        for i in go_list: # for each go term
            new_set = set([i])
            old_set = set()
            while len(new_set) != len(old_set): # trace back through go heirachy to see if it is a biological process
                old_set = new_set
                new_set = set()
                for j in old_set:
                    new_set.add(j)
                    try:
                        for k in go_rel_dict[j]:
                            new_set.add(k)
                    except KeyError:
                        pass
            if parent_go in new_set: # and then append it to list of new go terms
                new_go_list.append(i)
        print len(go_list)
        go_list = new_go_list
    print len(go_list)
    for i in gene_go: # if go term has been filtered check the other box
        for j in list(gene_go[i]):
            if not j in go_list:
                gene_go[i].add('other')
    the_array = numpy.zeros((len(gene_list), len(go_list)))
    for num1, i in enumerate(gene_list): # create array of go categories to box to cluster GO categories
        for num2, j in enumerate(go_list):
            if i in gene_go and j in gene_go[i]:
                the_array[num1][num2] = 1
    df = pandas.DataFrame(the_array)
    cluster = sns.clustermap(df)
    sv_gene_list = []
    sv_gene_nums = []
    plas_gene_list = []
    plas_gene_nums = []
    snv_gene_list = []
    added = set()
    if not only_snvs:
        for num, i in enumerate(cluster.dendrogram_row.reordered_ind):
            the_gene_name = gene_list[i]
            for j in sv_groups:
                if the_gene_name in j:
                    gc = 0
                    for k in j:
                        if not k in added and k in gene_list:
                            sv_gene_list.append(k)
                            added.add(k)
                            gc += 1
                    if gc != 0:
                        sv_gene_nums.append(gc)
        for num, i in enumerate(cluster.dendrogram_row.reordered_ind):
            the_gene_name = gene_list[i]
            for j in plasmid_groups:
                if the_gene_name in j:
                    gc = 0
                    for k in j:
                        if not k in added and k in gene_list:
                            plas_gene_list.append(k)
                            added.add(k)
                            gc += 1
                    if gc != 0:
                        plas_gene_nums.append(gc)
    for num, i in enumerate(cluster.dendrogram_row.reordered_ind):
        the_gene_name = gene_list[i]
        if not the_gene_name in added:
            snv_gene_list.append(the_gene_name)
    svg.drawLine(5, top_buffer + 0.1 * square_height, 5, top_buffer + (len(snv_gene_list) - 0.1) * square_height)
    svg.drawLine(5, top_buffer + (len(snv_gene_list) + 0.1) * square_height, 5, top_buffer + (len(snv_gene_list) + len(sv_gene_list) - 0.1) * square_height)
    svg.drawLine(5, top_buffer + (len(snv_gene_list) + len(sv_gene_list) + 0.1) * square_height, 5, top_buffer + (len(snv_gene_list) + len(sv_gene_list) + len(plas_gene_list) - 0.1) * square_height)
    curr_num = len(snv_gene_list)
    line_col = (200, 0, 0)
    for i in sv_gene_nums + plas_gene_nums:
        svg.drawLine(10, top_buffer + (curr_num + 0.1) * square_height, 10, top_buffer + (curr_num + i - 0.1) * square_height, th=5, cl=line_col)
        curr_num += i
        if line_col == (200, 0, 0):
            line_col = (0, 0, 200)
        else:
            line_col = (200, 0, 0)
    if only_snvs:
        gene_list = snv_gene_list
    else:
        gene_list = snv_gene_list + sv_gene_list + plas_gene_list
    new_go_list = []
    for i in cluster.dendrogram_col.reordered_ind:
        new_go_list.append(go_list[i])
    go_list = new_go_list
    go_list.append('other')
    go_descriptions['other'] = 'n/a'
    for num, i in enumerate(gene_list):

        svg.writeString(i, grid_start - 10, top_buffer + num * square_height + 0.75 * square_height, 10, justify='right')
        svg.writeString(description_dict[i][0], grid_start + (len(out_dict) + len(go_list)) * square_width + 20, top_buffer + num * square_height + 0.75 * square_height, 10)
        if not description_dict[i][1].startswith('PF'):
            test_out.write(description_dict[i][1] + '\n')
    svg.writeString('Phage genes:', grid_start - 10, top_buffer + (len(gene_list))* square_height + 0.75 * square_height, 10, justify='right')
    svg.writeString('Hypothetical proteins:', grid_start - 10, top_buffer + (len(gene_list) + 1) * square_height + 0.75 * square_height, 10, justify='right')


    ref_color = {
        'MRSA_pt158_B_196_ilm_reorient_chromosome':(205,198,70),
        'MRSA_pt152_F_629_ilm_reorient_chromosome':(122,196,131),
        'MRSA_pt152_B_187_ilm_reorient_chromosome':(122,196,131),
        'MRSA_pt135_F_546_ilm_reorient_chromosome':(187,143,155),
        'MRSA_pt135_B_165_ilm_reorient_chromosome':(187,143,155),
        'MRSA_pt117_F_468_ilm_reorient_chromosome':(132,138,211),
        'MRSA_pt117_B_143_ilm_reorient_chromosome':(132,138,211),
        'MRSA_pt108_B_128_ilm_reorient_chromosome':(217,103,56),
        'MRSA_pt073_B_085_ilm_reorient_chromosome':(169,148,90),
        'MRSA_pt060_B_061_ilm_reorient_chromosome':(201,92,203),
        'MRSA_pt053_B_054_ilm_reorient_chromosome':(134,190,189),
        'MRSA_pt045_B_045_ilm_reorient_chromosome':(112,207,70),
        'MRSA_pt035_B_027_ilm_reorient_chromosome':(217,83,119)
    }
    var_color = {
        'full_del':(217,70,42),#

        'full_ins':(87,198,57),#

        'nonsyn_query':(215,64,146),
        'nonsyn_amb':(224,126,173),
        'inframe_del_query':(95,131,220),
        'inframe_ins_query':(95,131,220),


        'nonsyn_query_stop':(199,164,49),
        'partial_del':(227,133,51),
        'partial_ins':(156,186,58),

        'syn_ref':(200,200,200),
        'syn_query':(200,200,200),
        'nonsyn_ref':(255, 255, 255),
        'nonsyn_ref_stop':(255, 255, 255),


        'deletion_query':(104,128,0),
        'insertion_query':(104,128,0),

        'mult':(148,110,209),#

        'present':(86,173,208)#
    }

    svg.writeString('Absent in query and reference', grid_start - 10, top_buffer + (len(gene_list) + 4) * square_height + 0.75 * square_height, 10, justify='right')
    svg.writeString('Present in query and reference (no change)', grid_start - 10, top_buffer + (len(gene_list) + 5) * square_height + 0.75 * square_height, 10, justify='right')
    svg.writeString('Deleted in query', grid_start - 10, top_buffer + (len(gene_list) + 6) * square_height + 0.75 * square_height, 10, justify='right')
    svg.writeString('Inserted in query', grid_start - 10, top_buffer + (len(gene_list) + 7) * square_height + 0.75 * square_height, 10, justify='right')
    svg.writeString('Nonsynonymous mutation (ancestral)', grid_start - 10, top_buffer + (len(gene_list) + 8) * square_height + 0.75 * square_height, 10, justify='right')
    svg.writeString('Nonsynonymous mutation (no ancestor)', grid_start - 10, top_buffer + (len(gene_list) + 9) * square_height + 0.75 * square_height, 10, justify='right')
    svg.writeString('Nonsynonymous mutation (stop codon)', grid_start - 10, top_buffer + (len(gene_list) + 10) * square_height + 0.75 * square_height, 10, justify='right')
    svg.writeString('in-frame indel', grid_start - 10, top_buffer + (len(gene_list) + 11) * square_height + 0.75 * square_height, 10, justify='right')
    svg.writeString('frameshift indel', grid_start - 10, top_buffer + (len(gene_list) + 12) * square_height + 0.75 * square_height, 10, justify='right')
    svg.writeString('Partial deletion', grid_start - 10, top_buffer + (len(gene_list) + 13) * square_height + 0.75 * square_height, 10, justify='right')
    svg.writeString('Partial insertion', grid_start - 10, top_buffer + (len(gene_list) + 14) * square_height + 0.75 * square_height, 10, justify='right')
    svg.writeString('More than one change', grid_start - 10, top_buffer + (len(gene_list) + 15) * square_height + 0.75 * square_height, 10, justify='right')
    svg.writeString('Synonymous change', grid_start - 10, top_buffer + (len(gene_list) + 16) * square_height + 0.75 * square_height, 10, justify='right')
    svg.writeString('Nonsynonymous mutation (in nares)', grid_start - 10, top_buffer + (len(gene_list) + 17) * square_height + 0.75 * square_height, 10, justify='right')

    svg.drawOutRect(grid_start, top_buffer + (len(gene_list) + 4) * square_height, 9, 9, lt=0, fill=(0,0,0))
    svg.drawOutRect(grid_start, top_buffer + (len(gene_list) + 5) * square_height, 9, 9, lt=0, fill=var_color['present'])
    svg.drawOutRect(grid_start, top_buffer + (len(gene_list) + 6) * square_height, 9, 9, lt=0, fill=var_color['full_del'])
    svg.drawOutRect(grid_start, top_buffer + (len(gene_list) + 7) * square_height, 9, 9, lt=0, fill=var_color['full_ins'])
    svg.drawOutRect(grid_start, top_buffer + (len(gene_list) + 8) * square_height, 9, 9, lt=0, fill=var_color['nonsyn_query'])
    svg.drawOutRect(grid_start, top_buffer + (len(gene_list) + 9) * square_height, 9, 9, lt=0, fill=var_color['nonsyn_amb'])
    svg.drawOutRect(grid_start, top_buffer + (len(gene_list) + 10) * square_height, 9, 9, lt=0, fill=var_color['nonsyn_query_stop'])
    svg.drawOutRect(grid_start, top_buffer + (len(gene_list) + 11) * square_height, 9, 9, lt=0, fill=var_color['inframe_del_query'])
    svg.drawOutRect(grid_start, top_buffer + (len(gene_list) + 12) * square_height, 9, 9, lt=0, fill=var_color['deletion_query'])
    svg.drawOutRect(grid_start, top_buffer + (len(gene_list) + 13) * square_height, 9, 9, lt=0, fill=var_color['partial_del'])
    svg.drawOutRect(grid_start, top_buffer + (len(gene_list) + 14) * square_height, 9, 9, lt=0, fill=var_color['partial_ins'])
    svg.drawOutRect(grid_start, top_buffer + (len(gene_list) + 15) * square_height, 9, 9, lt=0, fill=var_color['mult'])
    svg.drawOutRect(grid_start, top_buffer + (len(gene_list) + 16) * square_height, 9, 9, lt=0, fill=var_color['syn_ref'])
    svg.drawOutRect(grid_start, top_buffer + (len(gene_list) + 17) * square_height, 9, 9, lt=1, fill=var_color['nonsyn_ref_stop'])

    svg.writeString('Gene altered in pt035', grid_start - 10, top_buffer + (len(gene_list) + 24) * square_height + 0.75 * square_height, 10, justify='right')
    svg.writeString('Gene altered in pt045', grid_start - 10, top_buffer + (len(gene_list) + 25) * square_height + 0.75 * square_height, 10, justify='right')
    svg.writeString('Gene altered in pt108', grid_start - 10, top_buffer + (len(gene_list) + 26) * square_height + 0.75 * square_height, 10, justify='right')
    svg.writeString('Gene altered in pt152', grid_start - 10, top_buffer + (len(gene_list) + 27) * square_height + 0.75 * square_height, 10, justify='right')
    svg.writeString('Gene altered in pt158', grid_start - 10, top_buffer + (len(gene_list) + 28) * square_height + 0.75 * square_height, 10, justify='right')
    svg.writeString('Gene altered in pt053', grid_start - 10, top_buffer + (len(gene_list) + 29) * square_height + 0.75 * square_height, 10, justify='right')
    svg.writeString('Gene altered in pt060', grid_start - 10, top_buffer + (len(gene_list) + 30) * square_height + 0.75 * square_height, 10, justify='right')
    svg.writeString('Gene altered in pt073', grid_start - 10, top_buffer + (len(gene_list) + 31) * square_height + 0.75 * square_height, 10, justify='right')
    svg.writeString('Gene altered in pt117', grid_start - 10, top_buffer + (len(gene_list) + 32) * square_height + 0.75 * square_height, 10, justify='right')
    svg.writeString('Gene altered in pt135', grid_start - 10, top_buffer + (len(gene_list) + 33) * square_height + 0.75 * square_height, 10, justify='right')
    svg.writeString('Gene altered in multiple patients', grid_start - 10, top_buffer + (len(gene_list) + 34) * square_height + 0.75 * square_height, 10, justify='right')


    svg.drawOutRect(grid_start, top_buffer + (len(gene_list) + 24) * square_height, 9, 9, lt=0, fill=ref_color['MRSA_pt035_B_027_ilm_reorient_chromosome'])
    svg.drawOutRect(grid_start, top_buffer + (len(gene_list) + 25) * square_height, 9, 9, lt=0, fill=ref_color['MRSA_pt045_B_045_ilm_reorient_chromosome'])
    svg.drawOutRect(grid_start, top_buffer + (len(gene_list) + 26) * square_height, 9, 9, lt=0, fill=ref_color['MRSA_pt108_B_128_ilm_reorient_chromosome'])
    svg.drawOutRect(grid_start, top_buffer + (len(gene_list) + 27) * square_height, 9, 9, lt=0, fill=ref_color['MRSA_pt152_B_187_ilm_reorient_chromosome'])
    svg.drawOutRect(grid_start, top_buffer + (len(gene_list) + 28) * square_height, 9, 9, lt=0, fill=ref_color['MRSA_pt158_B_196_ilm_reorient_chromosome'])
    svg.drawOutRect(grid_start, top_buffer + (len(gene_list) + 29) * square_height, 9, 9, lt=0, fill=ref_color['MRSA_pt053_B_054_ilm_reorient_chromosome'])
    svg.drawOutRect(grid_start, top_buffer + (len(gene_list) + 30) * square_height, 9, 9, lt=0, fill=ref_color['MRSA_pt060_B_061_ilm_reorient_chromosome'])
    svg.drawOutRect(grid_start, top_buffer + (len(gene_list) + 31) * square_height, 9, 9, lt=0, fill=ref_color['MRSA_pt073_B_085_ilm_reorient_chromosome'])
    svg.drawOutRect(grid_start, top_buffer + (len(gene_list) + 32) * square_height, 9, 9, lt=0, fill=ref_color['MRSA_pt117_B_143_ilm_reorient_chromosome'])
    svg.drawOutRect(grid_start, top_buffer + (len(gene_list) + 33) * square_height, 9, 9, lt=0, fill=ref_color['MRSA_pt135_B_165_ilm_reorient_chromosome'])
    svg.drawOutRect(grid_start, top_buffer + (len(gene_list) + 34) * square_height, 9, 9, lt=0, fill=(0, 0, 100))

    out_list = list(out_dict)
    out_list.sort()
    new_out_list = []
    for i in ['pt035', 'pt045', 'pt108', 'pt152', 'pt158', 'pt053', 'pt060', 'pt073', 'pt117', 'pt135']:
        for j in out_list:
            if i in j:
                new_out_list.append(j)
    out_list = new_out_list
    for num, i in enumerate(out_list):
        phage_count = 0
        hypo_count = 0
        for j in out_dict[i]:
            if j in phage_set and out_dict[i][j] != 'present' and j in gene_list:
                phage_count += 1
            if j in hypo_set and out_dict[i][j] != 'present' and j in gene_list:
                hypo_count += 1
        svg.writeString(str(phage_count), grid_start + num * square_width + square_width/2, top_buffer + (len(gene_list)) * square_height + 0.75 * square_height, 6, justify='middle')
        svg.writeString(str(hypo_count), grid_start + num * square_width + square_width/2, top_buffer + (len(gene_list) + 1) * square_height + 0.75 * square_height, 6, justify='middle')
    ref_go = {}

    adj_set = set()
    for num1, i in enumerate(out_list):
        ref_go[i] = set()
        svg.writeString(i, grid_start + num1 * square_width, top_buffer-10, 10, justify='right', rotate=-1)
        for num2, j in enumerate(gene_list):
            if j in out_dict[i]:
                adj_genes = get_adjacent_genes(j, gen_folder, i)
                if adj_genes == []:
                    pass
                elif adj_genes[0] in gene_list:
                    adj_set.add((j, adj_genes[0]))
                elif adj_genes[1] in gene_list:
                    adj_set.add((j, adj_genes[1]))
                if not out_dict[i][j] == 'present':
                    if j in gene_go:
                        for q in gene_go[j]:
                            ref_go[i].add(q)
                if ',' in out_dict[i][j]:
                    color = var_color['mult']
                else:
                    color = var_color[out_dict[i][j]]
            else:
                color = (0, 0, 0)
            svg.drawOutRect(grid_start + num1 * square_width, top_buffer + num2 * square_height, square_width -1, square_height -1, fill=color, lt=0)
    for i in adj_set:
        print i
    table1 = open(out_label + '.table1.tsv', 'w')
    table1.write('gene\tinference\thomologs\tgene ontology')
    for j in out_list:
        table1.write('\t' + j)
    go_enrich = {}
    for i in old_gene_list:
        if i in gene_list and description_dict[i][1] != 'none' and not description_dict[i][1].startswith('PF'):
            if description_dict[i][1] in go_enrich:
                go_enrich[description_dict[i][1]] += 1

            else:
                go_enrich[description_dict[i][1]] = 1
        table1.write('\n' + i + '\t' + description_dict[i][1])
        if i in homolog and homolog[i] != []:
            table1.write('\t' + ','.join(homolog[i]))
        else:
            table1.write('\tnone')
        if i in gene_go:
            table1.write('\t' + ','.join(gene_go[i]))
        else:
            table1.write('\tnone')
        for j in out_list:
            if i in out_dict[j]:
                table1.write('\t' + out_dict[j][i])
            else:
                table1.write('\tgene absent')
    blurk = open('goenrich.tsv', 'w')
    for i in go_enrich:
        blurk.write(i + '\t' + str(go_enrich[i]) + '\n')
    table3 = open(out_label + 'table3.tsv', 'w')
    for i in count_var_set:
        table3.write('\t' + i)
    for i in count_dict:
        table3.write('\n' + i)
        for j in count_var_set:
            if j in count_dict[i]:
                table3.write('\t' + str(count_dict[i][j]))
            else:
                table3.write('\t0')
    go_freq['other'] = 'n/a'
    for num, i in enumerate(go_list):
        svg.writeString(i, grid_start + len(out_dict) * square_width + 10 + num * square_width, top_buffer-10, 10, justify='right', rotate=-1)
        svg.writeString(str(go_freq[i]) + ': ' +go_descriptions[i], grid_start + len(out_dict) * square_width + 10 + num * square_width, len(gene_list) * square_height + 10 + top_buffer, 10, rotate=-1)
    for num1, i in enumerate(gene_list):
        for j in adj_genes:
            if j in gene_list:
                print i, j
        if num1 % 5 == 0:
            svg.drawLine(grid_start, num1 * square_height + top_buffer - 0.5, grid_start + len(out_dict) * square_width + 10 + len(go_list) * square_width, num1 * square_height + top_buffer - 0.5)
        for num2, j in enumerate(go_list):
            if num1 == 0 and num2 % 5 == 0:
                svg.drawLine(grid_start + len(out_dict) * square_width + 10 + num2 * square_width - 0.5, top_buffer, grid_start + len(out_dict) * square_width + 10 + num2 * square_width - 0.5, top_buffer + len(gene_list) * square_height)
            if i in gene_go and j in gene_go[i]:
                in_ref = []
                for k in out_dict:
                    if i in out_dict[k] and out_dict[k][i] != 'present':
                        in_ref.append(k)
                if len(set(map(lambda qq: qq[:10], in_ref))) == 1:
                    color = ref_color[in_ref[0]]
                else:
                    color = (0, 0, 100)
               # svg.drawOutRect(grid_start + len(out_dict) * square_width + 10 + num2 * square_width, top_buffer + num1 * square_height, square_width -1, square_height -1, fill=color, lt=0)
            else:
                color = (220, 220, 220)
            svg.drawOutRect(grid_start + len(out_dict) * square_width + 10 + num2 * square_width, top_buffer + num1 * square_height, square_width -1, square_height -1, fill=color, lt=0)
    # for num1, i in enumerate(out_list):
    #     for num2, j in enumerate(go_list):
    #         if j in ref_go[i]:
    #             color = (0, 0, 200)
    #         else:
    #             color = (200, 0, 0)
    #         svg.drawOutRect(grid_start + num1 * square_width, top_buffer + len(gene_list) * square_height + 20 + num2 * square_height, square_width -1, square_height -1, fill=color, lt=0)

    svg.writesvg(out_label + '.svg')





get_genes(sys.argv[1], sys.argv[2], sys.argv[3])







