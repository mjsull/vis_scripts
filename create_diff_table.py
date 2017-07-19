import subprocess
import sys
import argparse
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



class alignment:
    def __init__(self):
        self.start_dict = {}
        self.stop_dict = {}
        self.seq_dict = {}
        self.strand_dict = {}

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

class gene:
    def __init__(self, start_stop):
        if start_stop.startswith('complement('):
            start, stop = start_stop[11:-1].split('..')
            self.start = int(start)
            self.stop = int(stop)
            self.strand = '-'
        else:
            start, stop = start_stop.split('..')
            self.start = int(start)
            self.stop = int(stop)
            self.strand = '+'
# get genes in a genbank file
def get_genes(genbank):
    gene_list = []
    get_seq = False
    with open(genbank) as gbk:
        for line in gbk:
            if line.startswith('     CDS    '):
                aninstance = gene(line.split()[1])
                gene_list.append(aninstance)
            elif line.startswith('                     /gene="'):
                gene_list[-1].name = line.split('"')[1]
            elif line.startswith('                     /locus_tag='):
                gene_list[-1].locus = line.split('"')[1]
            elif line.startswith('ORIGIN'):
                get_seq = True
                outseq = ''
            elif line.startswith('//'):
                get_seq = False
            elif get_seq:
                outseq += ''.join(line.split()[1:])
    return gene_list, outseq
# get alignments from a MAF file genereated by mugsy - this is used to convert ancestral information from PAML
# to an actual genome coordinate
def get_alignments(mugsy_file, num_gen):
    getit = False
    with open(mugsy_file) as mf:
        aninstance = alignment()
        for line in mf:
            if line.startswith('a'):
                splitline = line.split()
                mult = int(splitline[3].split('=')[1])
                if mult == int(num_gen):
                    getit = True
                else:
                    getit = False
            elif line.startswith('s') and getit:
                splitline = line.split()
                src = splitline[1]
                fasta = src.split('.')[0]
                contig = src.split('.')[1]
                start = int(splitline[2])
                size = int(splitline[3])
                strand = splitline[4]
                srcSize = int(splitline[5])
                nucl = splitline[6]
                if strand == '-':
                    start = srcSize - start - size
                if not fasta in aninstance.start_dict:
                    aninstance.start_dict[fasta] = [start]
                    aninstance.stop_dict[fasta] = [start + size]
                    aninstance.seq_dict[fasta] = [nucl]
                    aninstance.strand_dict[fasta] = [strand]
                else:
                    aninstance.start_dict[fasta].append(start)
                    aninstance.stop_dict[fasta].append(start + size)
                    aninstance.seq_dict[fasta].append(nucl)
                    aninstance.strand_dict[fasta].append(strand)
    return aninstance

# get the ancestral sequence for a particular node
def get_ancestral_sequence(rst, label):
    with open(rst) as paml:
        getit = 0
        anc_seq = ''
        for line in paml:
            if line.startswith('   site   Freq   Data: '):
                getit =1
            elif getit == 1:
                getit = 2
            elif getit == 2:
                try:
                    anc_seq += line.split()[label + 3].split('(')[0]
                except IndexError:
                    getit = 0
    return anc_seq


# get differecnes between two genbank files using nucmer
def get_diff(gbk1, gbk2, working_dir, out_file, alignment, anc_seq, genes1, genes2, first_seq, second_seq):
    merge_snp_size = 0
    if not os.path.exists(working_dir):
        os.makedirs(working_dir)
    q_name = gbk2.split('/')[-1].split('.')[0]
    with open(working_dir + '/' + q_name + '.fa', 'w') as out:
        out.write('>' + q_name + '\n')
        out.write(second_seq)
    r_name = gbk1.split('/')[-1].split('.')[0]
    with open(working_dir + '/' + r_name + '.fa', 'w') as out:
        out.write('>' + r_name + '\n')
        out.write(first_seq)
    subprocess.Popen('nucmer --breaklen=20 --prefix=' + working_dir + '/' + r_name + '_' + q_name + ' ' +
                     working_dir + '/' + r_name + '.fa ' + working_dir + '/' + q_name + '.fa', shell=True, stderr=subprocess.PIPE).wait()
    subprocess.Popen('delta-filter -g ' + working_dir + '/' + r_name + '_' + q_name + '.delta > ' +
                     working_dir + '/' + r_name + '_' + q_name + '.filter.delta', shell=True, stderr=subprocess.PIPE).wait()
    subprocess.Popen('delta-filter -r ' + working_dir + '/' + r_name + '_' + q_name + '.delta > ' +
                     working_dir + '/' + r_name + '_' + q_name + '.r.filter.delta', shell=True, stderr=subprocess.PIPE).wait()
    subprocess.Popen('delta-filter -q ' + working_dir + '/' + r_name + '_' + q_name + '.delta > ' +
                     working_dir + '/' + r_name + '_' + q_name + '.q.filter.delta', shell=True, stderr=subprocess.PIPE).wait()
    subprocess.Popen('show-snps -Tlr ' + working_dir + '/' + r_name + '_' + q_name + '.filter.delta > ' + working_dir + '/' + r_name + '_' + q_name + '.snps',
                     shell=True, stderr=subprocess.PIPE).wait()
    subprocess.Popen('show-coords -r ' + working_dir + '/' + r_name + '_' + q_name + '.filter.delta > ' + working_dir +
                     '/' + r_name + '_' + q_name + '.filtered.coords', shell=True, stderr=subprocess.PIPE).wait()
    subprocess.Popen('show-coords -r ' + working_dir + '/' + r_name + '_' + q_name + '.r.filter.delta > ' + working_dir +
                     '/' + r_name + '_' + q_name + '.r.filtered.coords', shell=True, stderr=subprocess.PIPE).wait()
    subprocess.Popen('show-coords -r ' + working_dir + '/' + r_name + '_' + q_name + '.q.filter.delta > ' + working_dir +
                     '/' + r_name + '_' + q_name + '.q.filtered.coords', shell=True, stderr=subprocess.PIPE).wait()
    out_tsv = open(out_file, 'w')
    out_tsv.write('\t'.join(['type', 'query_name', 'query_start', 'query_stop', 'reference_name', 'reference_start',
                             'reference_stop', 'query base/size', 'reference base/size', 'ancestor_base_size',
                             'type', 'in_gene_q', 'in_gene_r', 'overlap_gene_q', 'overlap_gene_r', 'contains_gene_q', 'contains_gene_r',
                            'nearest_upstream_q', 'nearest_upstream_r', 'nearest_downstream_q', 'nearest_downstream_r']) + '\n')
    ignored_char = set(['N', '-'])
    with open(working_dir + '/' + r_name + '_' + q_name + '.snps') as snps:
        get_snp_lines = False
        last_del = None
        snp_list = []
        for line in snps:
            if line.startswith('[P1]'):
                get_snp_lines = True
            elif get_snp_lines:
                pos1, b1, b2, pos2, buff, dist, rr, rq, lenr, lenq, fr, tag, name1, name2 = line.split()
                the_pos1 = int(pos1)
                the_pos2 = int(pos2)
                if snp_list != [] and the_pos1 >= snp_list[-1][1] and the_pos2 >= snp_list[-1][3] and \
                        (snp_list[-1][1] >= the_pos1 - merge_snp_size or snp_list[-1][3] >= the_pos2 - merge_snp_size):
                    if snp_list[-1][0] == the_pos1:
                        snp_list[-1][4] = '.'
                    else:
                        snp_list[-1][4] = first_seq[snp_list[-1][0]-1:the_pos1].upper()
                    if snp_list[-1][2] == the_pos2:
                        snp_list[-1][5] = '.'
                    else:
                        snp_list[-1][5] = second_seq[snp_list[-1][2]-1:the_pos2].upper()
                    snp_list[-1][1] = the_pos1
                    snp_list[-1][3] = the_pos2
                else:
                    snp_list.append([the_pos1, the_pos1, the_pos2, the_pos2, b1, b2])
    dna_file = open(out_file + '.faa', 'w')
    for snp in snp_list:
        startpos1, endpos1, startpos2, endpos2, b1, b2 = snp
        if b1 == '.' or b2 == '.' or len(b1) != len(b2):
            ancestor_base = 'indel'
        elif not anc_seq is None:
            for i in alignment.start_dict:
                if name1.startswith(i[:-5]):
                    dict_name_1 = i
                if name2.startswith(i[:-5]):
                    dict_name_2 = i
            gotit = False
            curr_seq_dict = {}
            ancestor_base = None
            for i in alignment.start_dict:
                curr_seq_dict[i] = ''
            for i in range(len(alignment.start_dict[dict_name_1])):
                start1, stop1, strand1, seq1 = alignment.start_dict[dict_name_1][i], alignment.stop_dict[dict_name_1][i],\
                                               alignment.strand_dict[dict_name_1][i], alignment.seq_dict[dict_name_1][i]
                start2, stop2, strand2, seq2 = alignment.start_dict[dict_name_2][i], alignment.stop_dict[dict_name_2][i],\
                                               alignment.strand_dict[dict_name_2][i], alignment.seq_dict[dict_name_2][i]
                if start1 <= startpos1 <= endpos1 <= stop1 and start2 <= startpos2 <= endpos2 <= stop2:
                    gotit = True
                    if strand1 == '+':
                        a_pos = start1
                        for j in range(len(seq1)):
                            if seq1[j] != '-':
                                a_pos += 1
                                if a_pos == endpos1:
                                    pos_in_align = j
                                    break
                    else:
                        a_pos = start1
                        for j in range(len(seq1)):
                            if seq1[::-1][j] != '-':
                                a_pos += 1
                                if a_pos == endpos1:
                                    pos_in_align = len(seq1) - j
                                    break
                    if strand2 == '+':
                        a_pos = start2
                        for j in range(len(seq2)):
                            if seq2[j] != '-':
                                a_pos += 1
                                if a_pos == endpos2:
                                    if j == pos_in_align:
                                        for k in curr_seq_dict:
                                            curr_seq_dict[k] += alignment.seq_dict[k][i][:pos_in_align+1]
                                    else:
                                        ancestor_base = 'ambiguous alignment'
                                      #  sys.exit()
                                    break
                    else:
                        a_pos = start2
                        for j in range(len(seq2)):
                            if seq2[::-1][j] != '-':
                                a_pos += 1
                                if a_pos == endpos2:
                                    if len(seq2) - j == pos_in_align:
                                        for k in curr_seq_dict:
                                            curr_seq_dict[k] += alignment.seq_dict[k][i][:pos_in_align+1]
                                    else:
                                        ancestor_base = 'ambiguous alignment'
                                       # sys.exit()
                                    break
                    paml_pos = 0
                    lastdel = False
                    var_size = endpos1 - startpos1 + 1
                    if ancestor_base is None:
                        for l in curr_seq_dict:
                            if '-' in curr_seq_dict[l][-var_size:]:
                                lastdel = True
                    if lastdel:
                        ancestor_base = 'del_at_spot'
                    elif ancestor_base is None:
                        test_seq = {}
                        for l in curr_seq_dict:
                            test_seq[l] = ''
                        for k in range(len(curr_seq_dict[dict_name_1])):
                            inc_it = True
                            for l in curr_seq_dict:
                                if curr_seq_dict[l][k] in ignored_char:
                                    inc_it = False
                                    break
                            if inc_it:
                                paml_pos += 1
                        ancestor_base = anc_seq[paml_pos-var_size:paml_pos]
                    break
                elif start1 <= startpos1 <= endpos1 <= stop1 or start2 <= startpos2 <= endpos2 <= stop2:
                    gotit = True
                    ancestor_base = 'misaligned'
                    break
                else:
                    for j in alignment.seq_dict:
                        curr_seq_dict[j] += alignment.seq_dict[j][i]
            if not gotit:
                ancestor_base = 'unaligned'
        else:
            ancestor_base = 'no_paml'
        mut_type = None
        in_q = []
        cont_q = []
        over_q = []
        up_q = None
        down_q = None
        genes1.sort(key=lambda x:x.start)
        genes2.sort(key=lambda x:x.start)
        last_gene = 'none'
        for i in genes1:
            try:
                genestring = i.name + ','
            except:
                genestring = 'none,'
            genestring += i.locus + ',' + i.strand + ',' + str(i.start) + '..' + str(i.stop) + ',' + str(startpos1 - i.start)\
            + '/' + str(i.stop - i.start)
            if i.start <= startpos1 <= endpos1 <= i.stop:
                if up_q is None:
                    up_q = last_gene
                in_q.append(genestring)
                if len(ancestor_base) == 1 and ancestor_base != b1 and ancestor_base != b2:
                    print ancestor_base, b1, b2, q_name
                    print 'ancestor base not in either'
                if b2 == ancestor_base:
                    mod_seq = first_seq[:startpos1-1] + ancestor_base + first_seq[endpos1:]
                    if i.strand == '+':
                        if translate_dna(first_seq[i.start-1:i.stop]) == translate_dna(mod_seq[i.start-1:i.stop]):
                            mut_type = 'syn_query'
                        elif translate_dna(mod_seq[i.start-1:i.stop])[-1] != '*':
                            mut_type = 'nonsyn_query_stop_gain'
                        elif '*' in translate_dna(mod_seq[i.start-1:i.stop])[:-1]:
                            mut_type = 'nonsyn_query_stop_loss'
                        else:
                            mut_type = 'nonsyn_query'
                            dna_file.write('>' + i.locus + ',que,' + str(startpos2) + '\n' + translate_dna(first_seq[i.start-1:i.stop])[:-1] + '\n')
                            dna_file.write('>' + i.locus + ',anc,' + str(startpos2) + '\n' + translate_dna(mod_seq[i.start-1:i.stop])[:-1] + '\n')
                    else:
                        if translate_dna(reverse_compliment(first_seq[i.start-1:i.stop])) == \
                                translate_dna(reverse_compliment(mod_seq[i.start-1:i.stop])):
                            mut_type = 'syn_query'
                        elif translate_dna(reverse_compliment(mod_seq[i.start-1:i.stop]))[-1] != '*':
                            mut_type = 'nonsyn_query_stop_gain'
                        elif '*' in translate_dna(reverse_compliment(mod_seq[i.start-1:i.stop]))[:-1]:
                            mut_type = 'nonsyn_query_stop_loss'
                        else:
                            mut_type = 'nonsyn_query'
                            dna_file.write('>' + i.locus + ',que,' + str(startpos2) + '\n' + translate_dna(reverse_compliment(first_seq[i.start-1:i.stop]))[:-1] + '\n')
                            dna_file.write('>' + i.locus + ',anc,' + str(startpos2) + '\n' + translate_dna(reverse_compliment(mod_seq[i.start-1:i.stop]))[:-1] + '\n')
                elif b1 == '.' and len(b2) % 3 == 0:
                    mut_type = 'inframe_del_query'
                elif b1 == '.':
                    mut_type = 'deletion_query'
                elif len(b1) < len(b2) and (len(b2) - len(b1)) % 3 == 0:
                    mut_type = 'inframe_del_query'
                elif len(b1) < len(b2):
                    mut_type = 'deletion_query'
                elif b2 == '.' and len(b1) % 3 == 0:
                    mut_type = 'inframe_ins_query'
                elif b2 == '.':
                    mut_type = 'insertion_query'
                elif len(b1) > len(b2) and (len(b1) - len(b2)) % 3 == 0:
                    mut_type = 'inframe_ins_query'
                elif len(b1) > len(b2):
                    mut_type = 'insertion_query'
                else:
                    mod_seq = first_seq[:startpos1-1] + b2 + first_seq[endpos1:]
                    if i.strand == '+':
                        if translate_dna(first_seq[i.start-1:i.stop]) == translate_dna(mod_seq[i.start-1:i.stop]):
                            mut_type = 'syn_amb'
                        else:
                            mut_type = 'nonsyn_amb'
                            if b1 != ancestor_base:
                                dna_file.write('>' + i.locus + ',que,' + str(startpos2) + '\n' + translate_dna(first_seq[i.start-1:i.stop][:-1]) + '\n')
                                dna_file.write('>' + i.locus + ',ref,' + str(startpos2) + '\n' + translate_dna(mod_seq[i.start-1:i.stop][:-1]) + '\n')
                    else:
                        if translate_dna(reverse_compliment(first_seq[i.start-1:i.stop])) == \
                                translate_dna(reverse_compliment(mod_seq[i.start-1:i.stop])):
                            mut_type = 'syn_amb'
                        else:
                            mut_type = 'nonsyn_amb'
                            if b1 != ancestor_base:
                                dna_file.write('>' + i.locus + ',que,' + str(startpos2) + '\n' + translate_dna(reverse_compliment(first_seq[i.start-1:i.stop]))[:-1] + '\n')
                                dna_file.write('>' + i.locus + ',ref,' + str(startpos2) + '\n' + translate_dna(reverse_compliment(mod_seq[i.start-1:i.stop]))[:-1] + '\n')
            elif startpos1 <= i.start <= i.stop <= endpos1:
                if up_q is None:
                    up_q = last_gene
                cont_q.append(genestring)
            elif i.start <= startpos1 <= i.stop or i.start <= endpos1 <= i.stop:
                if up_q is None:
                    up_q = last_gene
                over_q.append(genestring)
            elif i.start >= endpos1 and down_q is None:
                if up_q is None:
                    up_q = last_gene
                if i.strand == '+':
                    down_q = genestring
            if i.strand == '-':
                last_gene = genestring
        in_r = []
        cont_r = []
        over_r = []
        up_r = None
        down_r = None
        last_gene = 'none'
        for i in genes2:
            try:
                genestring = i.name + ','
            except:
                genestring = 'none,'
            genestring += i.locus + ',' + i.strand + ',' + str(i.start) + '..' + str(i.stop) + ',' + str(startpos2 - i.start)\
            + '/' + str(i.stop - i.start)
            if i.start <= startpos2 <= endpos2 <= i.stop:
                if up_r is None:
                    up_r = last_gene
                in_r.append(genestring)
                if b1 == ancestor_base:
                    mod_seq = second_seq[:startpos2-1] + ancestor_base + second_seq[endpos2:]
                    if i.strand == '+':
                        if translate_dna(second_seq[i.start-1:i.stop]) == translate_dna(mod_seq[i.start-1:i.stop]):
                            mut_type = 'syn_ref'
                        elif translate_dna(mod_seq[i.start-1:i.stop])[-1] != '*':
                            mut_type = 'nonsyn_ref_stop_gain'
                        elif '*' in translate_dna(mod_seq[i.start-1:i.stop])[:-1]:
                            mut_type == 'nonsyn_ref_stop_loss'
                        else:
                            # dna_file.write('>' + i.locus + ',ref,' + str(startpos2) + '\n' + translate_dna(second_seq[i.start-1:i.stop])[:-1] + '\n')
                            # dna_file.write('>' + i.locus + ',anc,' + str(startpos2) + '\n' + translate_dna(mod_seq[i.start-1:i.stop])[:-1] + '\n')
                            mut_type = 'nonsyn_ref'
                    else:
                        if translate_dna(reverse_compliment(second_seq[i.start-1:i.stop])) == \
                                translate_dna(reverse_compliment(mod_seq[i.start-1:i.stop])):
                            mut_type = 'syn_ref'
                        elif translate_dna(reverse_compliment(mod_seq[i.start-1:i.stop]))[-1] != '*':
                            mut_type = 'nonsyn_ref_stop_gain'
                        elif '*' in translate_dna(reverse_compliment(mod_seq[i.start-1:i.stop]))[:-1]:
                            mut_type = 'nonsyn_ref_stop_loss'
                        else:
                            # dna_file.write('>' + i.locus + ',ref,' + str(startpos2) + '\n' + translate_dna(reverse_compliment(second_seq[i.start-1:i.stop]))[:-1] + '\n')
                            # dna_file.write('>' + i.locus + ',anc,' + str(startpos2) + '\n' + translate_dna(reverse_compliment(mod_seq[i.start-1:i.stop]))[:-1] + '\n')
                            mut_type = 'nonsyn_ref'
                elif b1 == '.':
                    mut_type = 'deletion_query'
                elif b2 == '.':
                    mut_type = 'insertion_query'
            elif startpos2 <= i.start <= i.stop <= endpos2:
                if up_r is None:
                    up_r = last_gene
                cont_r.append(genestring)
            elif i.start <= startpos2 <= i.stop or i.start <= endpos2 <= i.stop:
                if up_r is None:
                    up_r = last_gene
                over_r.append(genestring)
            elif i.start >= endpos2 and down_r is None:
                if up_r is None:
                    up_r = last_gene
                if i.strand == '+':
                    down_r = genestring
            if i.strand == '-':
                last_gene = genestring
        if in_q == [] and in_r == []:
            if b1 == ancestor_base:
                mut_type = 'intergenic_ref'
            elif b2 == ancestor_base:
                mut_type = 'intergenic_query'
            else:
                mut_type = 'intergenic_amb'
        elif (in_q == [] or in_r == []):
            mut_type = 'no_matching_genes'
        if in_q == []:
            in_q = ['none']
        if in_r == []:
            in_r = ['none']
        if over_q == []:
            over_q = ['none']
        if over_r == []:
            over_r = ['none']
        if cont_q == []:
            cont_q = ['none']
        if cont_r == []:
            cont_r = ['none']
        out_tsv.write('\t'.join(map(str, ['Variant', r_name, startpos1, endpos1, q_name, startpos2, endpos2, b1, b2, ancestor_base, mut_type,
                                 ';'.join(in_q), ';'.join(in_r), ';'.join(over_q), ';'.join(over_r), ';'.join(cont_q), ';'.join(cont_r),
                                 up_q, up_r, down_q, down_r])) + '\n')
    q_coords = []
    with open(working_dir + '/' + r_name + '_' + q_name + '.q.filtered.coords') as coords:
        get_var_lines = False
        for line in coords:
            if line.startswith('================='):
                get_var_lines = True
                starts_align = None
                last_end1 = None
                last_end2 = None
            elif get_var_lines:
                s1, e1, bar, s2, e2, bar, len1, len2, bar, ident, bar, query, ref = line.split()
                s1, e1, s2, e2, len1, len2 = map(int, (s1, e1, s2, e2, len1, len2))
                q_coords.append((s1, e1, s2, e2, len1, len2))
    r_coords = []
    with open(working_dir + '/' + r_name + '_' + q_name + '.r.filtered.coords') as coords:
        get_var_lines = False
        for line in coords:
            if line.startswith('================='):
                get_var_lines = True
                starts_align = None
                last_end1 = None
                last_end2 = None
            elif get_var_lines:
                s1, e1, bar, s2, e2, bar, len1, len2, bar, ident, bar, query, ref = line.split()
                s1, e1, s2, e2, len1, len2 = map(int, (s1, e1, s2, e2, len1, len2))
                r_coords.append((s1, e1, s2, e2, len1, len2))
    with open(working_dir + '/' + r_name + '_' + q_name + '.filtered.coords') as coords:
        get_var_lines = False
        the_coords = []
        for line in coords:
            if line.startswith('================='):
                get_var_lines = True
                starts_align = None
                last_end1 = None
                last_end2 = None
            elif get_var_lines:
                s1, e1, bar, s2, e2, bar, len1, len2, bar, ident, bar, query, ref = line.split()
                s1, e1, s2, e2, len1, len2 = map(int, (s1, e1, s2, e2, len1, len2))
                the_coords.append((s1, e1, bar, s2, e2, bar, len1, len2, bar, ident, bar, query, ref))
    for line in the_coords:
        s1, e1, bar, s2, e2, bar, len1, len2, bar, ident, bar, query, ref = line
        in_q = []
        cont_q = []
        over_q = []
        up_q = None
        down_q = None
        in_r = []
        cont_r = []
        over_r = []
        up_r = None
        down_r = None
        last_gene = 'none'
        if not starts_align is None:
            for i in genes1:
                try:
                    genestring = i.name + ','
                except:
                    genestring = 'none,'
                genestring += i.locus + ',' + i.strand + ',' + str(i.start) + '..' + str(i.stop) + ',' + str(s1 - i.start)\
                + '/' + str(i.stop - i.start)
                if i.start <= s1 <= last_end1 <= i.stop or i.start <= last_end1 <= s1 <= i.stop:
                    if up_q is None:
                        up_q = last_gene
                    in_q.append(genestring)
                elif s1 <= i.start <= i.stop <= last_end1 or last_end1 <= i.start <= i.stop <= s1:
                    if up_q is None:
                        up_q = last_gene
                    cont_q.append(genestring)
                elif i.start <= s1 <= i.stop or i.start <= last_end1 <= i.stop:
                    if up_q is None:
                        up_q = last_gene
                    over_q.append(genestring)
                elif i.start >= s1 and down_q is None:
                    if up_q is None:
                        up_q = last_gene
                    if i.strand == '+':
                        down_q = genestring
                if i.strand == '-':
                    last_gene = genestring
            for i in genes2:
                try:
                    genestring = i.name + ','
                except:
                    genestring = 'none,'
                genestring += i.locus + ',' + i.strand + ',' + str(i.start) + '..' + str(i.stop) + ',' + str(s2 - i.start)\
                + '/' + str(i.stop - i.start)
                if i.start <= s2 <= last_end2 <= i.stop or i.start <= last_end2 <= s2 <= i.stop:
                    if up_r is None:
                        up_r = last_gene
                    in_r.append(genestring)
                elif s2 <= i.start <= i.stop <= last_end2 or last_end2 <= i.start <= i.stop <= s2:
                    if up_r is None:
                        up_r = last_gene
                    cont_r.append(genestring)
                elif i.start <= s2 <= i.stop or i.start <= last_end2 <= i.stop:
                    if up_r is None:
                        up_r = last_gene
                    over_r.append(genestring)
                elif i.start >= s2 and down_r is None:
                    if up_r is None:
                        up_r = last_gene
                    if i.strand == '+':
                        down_r = genestring
                if i.strand == '-':
                    last_gene = genestring
        if in_q == []:
            in_q = ['none']
        if in_r == []:
            in_r = ['none']
        if over_q == []:
            over_q = ['none']
        if over_r == []:
            over_r = ['none']
        if cont_q == []:
            cont_q = ['none']
        if cont_r == []:
            cont_r = ['none']
        if s1 == 1 and s2 == 1:
            starts_align = True
        elif s1 == 1 and starts_align is None:
            starts_align = ('2 overhang', s2)
            print '2 overhang'
        elif s2 == 1 and starts_align is None:
            starts_align = ('1 overhang', s1)
            print '1 overhang'
        elif starts_align is None:
            print 'mismatched start'
            starts_align = ('mismatched start', s1, s2)
        elif s1 == last_end1 + 1 and s2 > last_end2:
            svtype = 'deletion in query'
            p1, p2, p3, p4 = last_end1, s1, last_end2, s2
        elif (s1 == last_end1 + 1 and s2 < last_end2) or (s2 <= last_end2 and s1 <= last_end1 and last_end2 - s2 > last_end1 - s1):
            svtype = 'tandem expansion in query'
            p1, p2, p3, p4 = last_end1, s1, s2, last_end2
        elif s2 == last_end2 + 1 and s1 > last_end1:
            svtype = 'insertion in query'
            p1, p2, p3, p4 =  last_end1, s1, last_end2, s2
        elif (s2 == last_end2 + 1 and s1 < last_end1) or (s2 <= last_end2 and s1 <= last_end1 and last_end2 - s2 < last_end1 - s1):
            svtype = 'tandem contraction in query'
            p1, p2, p3, p4 = s1, last_end1, s2, last_end2
        elif s1 <= last_end1 and s2 > last_end2:
            svtype = 'deletion in query (duplicated ends)'
            p1, p2, p3, p4 = s1, last_end1, last_end2, s2
        elif s2 <= last_end2 and s1 > last_end1:
            svtype = 'insertion in query (duplicated ends)'
            p1, p2, p3, p4 = last_end1, s1, s2, last_end2
        elif s2 > last_end2 and s1 > last_end1:
            svtype = None
            for i in q_coords:
                if i[0] <= last_end1 + 1 and i[1] >= s1 - 1 and i[3] <= last_end2 + 1 and i[2] >= s2 - 1:
                    svtype = 'inversion'
            if svtype is None:
                svtype = 'Variable region'
            p1, p2, p3, p4 = last_end1, s1, last_end2, s2
        else:
            svtype = 'struct'
            p1, p2, p3, p4 = last_end1, s1, last_end2, s2
        if not last_end1 is None:
            out_tsv.write('\t'.join(map(str, ['SV', r_name, p1, p2, q_name, p3, p4, abs(p1 - p2), abs(p3 - p4), 'none', svtype,
                         ';'.join(in_q), ';'.join(in_r), ';'.join(over_q), ';'.join(over_r), ';'.join(cont_q), ';'.join(cont_r),
                         up_q, up_r, down_q, down_r])) + '\n')
        last_end2 = e2
        last_end1 = e1
    out_tsv.close()

# draw differences
def draw_diff(diff_file, length1, length2, q_name, r_name, out_file):
    top_buffer = 300
    bottom_buffer = 600
    ygap = 75
    genome_thick = 25
    snp_thick = 5
    sv_thick = 4
    join_thick = 2
    fig_width = 2000
    left_buffer = 300
    right_buffer = 800
    svg = scalableVectorGraphics(top_buffer + bottom_buffer + 2 * genome_thick + ygap, fig_width + left_buffer + right_buffer)
    max_width = 3000000
    highlight = 'query'
    anc_base_col = (193,130,45)
    anc_base_col_high = (245, 232, 214)
    anc_base_col_low = (245, 232, 214)
    nonsyn_col = (177, 98, 183)
    nonsyn_col_high = (135, 64, 140)
    nonsyn_col_low = (238, 220, 239)
    syn_col = (90, 147, 191)
    syn_col_low = (218, 231, 241)
    syn_col_high = (57, 108, 147)
    # dictionaries of colors to use for the figure
    if highlight == 'query':
        colourDictQuery = {
            'deletion_query':nonsyn_col,
            'insertion_query':nonsyn_col,
            'syn_ref':anc_base_col_low,
            'nonsyn_ref':anc_base_col_low,
            'syn_query':syn_col_high,
            'nonsyn_query':nonsyn_col_high,
            'syn_amb':syn_col,
            'nonsyn_amb':nonsyn_col,
            'intergenic_ref':anc_base_col_low,
            'intergenic_query':syn_col_high,
            'intergenic_amb':syn_col,
            'nonsyn_ref_stop_gain':anc_base_col_low,
            'nonsyn_ref_stop_loss':anc_base_col_low,
            'nonsyn_query_stop_gain':nonsyn_col_high,
            'nonsyn_query_stop_loss':nonsyn_col_high,
            'no_matching_genes':nonsyn_col
        }
        colourDictRef = {
            'deletion_query':nonsyn_col,
            'insertion_query':nonsyn_col,
            'syn_ref':syn_col_low,
            'nonsyn_ref':nonsyn_col_low,
            'syn_query':anc_base_col_high,
            'nonsyn_query':anc_base_col_high,
            'syn_amb':syn_col,
            'nonsyn_amb':nonsyn_col,
            'intergenic_ref':syn_col_low,
            'intergenic_query':anc_base_col_high,
            'intergenic_amb':syn_col,
            'nonsyn_ref_stop_gain':nonsyn_col_low,
            'nonsyn_ref_stop_loss':nonsyn_col_low,
            'nonsyn_query_stop_gain':anc_base_col_high,
            'nonsyn_query_stop_loss':anc_base_col_high,
            'no_matching_genes':nonsyn_col
        }
    elif highlight == 'ref':
        colourDictQuery = {
            'deletion_query':(184,110,188),
            'insertion_query':(184,110,188),
            'syn_ref':(193,130,45),
            'nonsyn_ref':(193,130,45),
            'syn_query':(89,147,190),
            'nonsyn_query':(184,110,188),
            'syn_amb':(89,147,190),
            'nonsyn_amb':(184,110,188),
            'intergenic_ref':(193,130,45),
            'intergenic_query':(89,147,190),
            'intergenic_amb':(89,147,190),
            'nonsyn_ref_stop':(193,130,45),
            'nonsyn_query_stop_gain':nonsyn_col_high,
            'nonsyn_query_stop_loss':nonsyn_col_high,
            'no_matching_genes':(184,110,188)
        }
        colourDictRef = {
            'deletion_query':(184,110,188),
            'insertion_query':(184,110,188),
            'syn_ref':(89,147,190),
            'nonsyn_ref':(184,110,188),
            'syn_query':(193,130,45),
            'nonsyn_que ry':(193,130,45),
            'syn_amb':(89,147,190),
            'nonsyn_amb':(184,110,188),
            'intergenic_ref':(89,147,190),
            'intergenic_query':(193,130,45),
            'intergenic_amb':(89,147,190),
            'nonsyn_ref_stop':(184,110,188),
            'nonsyn_query_stop_gain':nonsyn_col_high,
            'nonsyn_query_stop_loss':nonsyn_col_high,
            'no_matching_genes':(184,110,188)
        }
    else:
        colourDictQuery = {
            'deletion_query':(184,110,188),
            'insertion_query':(184,110,188),
            'syn_ref':(193,130,45),
            'nonsyn_ref':(193,130,45),
            'syn_query':(89,147,190),
            'nonsyn_query':(184,110,188),
            'syn_amb':(89,147,190),
            'nonsyn_amb ':(184,110,188),
            'intergenic_ref':(193,130,45),
            'intergenic_query':(89,147,190),
            'intergenic_amb':(89,147,190),
            'nonsyn_ref_stop':(193,130,45),
            'nonsyn_query_stop':(184,110,188),
            'no_matching_genes':(184,110,188)
        }
        colourDictRef = {
            'deletion_query':(184,110,188),
            'insertion_query':(184,110,188),
            'syn_ref':(89,147,190),
            'nonsyn_ref':(184,110,188),
            'syn_query':(193,130,45),
            'nonsyn_query':(193,130,45),
            'syn_amb':(89,147,190),
            'nonsyn_amb':(184,110,188),
            'intergenic_ref':(89,147,190),
            'intergenic_query':(193,130,45),
            'intergenic_amb':(89,147,190),
            'nonsyn_ref_stop':(184,110,188),
            'nonsyn_query_stop':(193,130,45),
            'no_matching_genes':(184,110,188)
        }
    colourDictSV = {'deletion in query':(211,78,92),
                    'tandem expansion in query':((105,173,76), (105,173,76)),
                    'insertion in query':(211,78,92),
                    'tandem contraction in query':((105,173,76), (105,173,76)),
                    'insertion in query (duplicated ends)':((211,78,92), (105,173,76)),
                    'deletion in query (duplicated ends)':((211,78,92), (105,173,76)),
                    'Variable region':(211,78,92),
                    'inversion':(211,78,92)
    }
    scale_bar_size = 3000000
    scale_bar_step = 500000
    svg.drawOutRect(left_buffer, top_buffer/2, int(scale_bar_size * 1.0 / max_width * fig_width), genome_thick, alpha2=0, lt=3)
    for i in range(scale_bar_step, scale_bar_size, scale_bar_step):
        svg.drawLine(left_buffer + int(i * 1.0 / max_width * fig_width), top_buffer/2, left_buffer + int(i * 1.0 / max_width * fig_width), top_buffer/2 + genome_thick, th=2)
        svg.writeString(str(i) + ' bp', left_buffer + int(i * 1.0 / max_width * fig_width), top_buffer/2 - 5, genome_thick/4, justify='middle')
    svg.drawOutRect(left_buffer, top_buffer, int(length2 * 1.0 / max_width * fig_width), genome_thick, alpha2=1, lt=0, fill=(200,200,200))
    svg.writeString(r_name, left_buffer + fig_width + right_buffer/30, top_buffer + genome_thick*4/6, genome_thick)
    svg.drawOutRect(left_buffer, top_buffer + ygap + genome_thick, int(length1 * 1.0 / max_width * fig_width), genome_thick, alpha2=1, lt=0, fill=(200,200,200))
    svg.writeString(q_name, left_buffer + fig_width + right_buffer/30, top_buffer + ygap + genome_thick + genome_thick*4/6, genome_thick)
    blast_overhang = 10
    blast_hit_overhang = 10 + sv_thick /2
    with open(diff_file) as df:
        for line in df:
#        for line in reversed(df.readlines()):
            if line.startswith('Variant'):
                stuff1, q_name, pos1, pos2, r_name, pos3, pos4, b1, b2, anc_type, mut_type, genes1, genes2, genes3, genes4, genes5, genes6, genes7, genes8, genes9, genes10 = line.split('\t')
                pos1, pos3 = int(pos1), int(pos3)
                x1 = int(pos1 * 1.0 / max_width * fig_width) + left_buffer
                x2 = int(pos3 * 1.0 / max_width * fig_width) + left_buffer
                join_color = (200, 200, 200)
                color1 = colourDictQuery[mut_type]
                color2 = colourDictRef[mut_type]
                svg.drawLine(x2, top_buffer + genome_thick, x1, top_buffer + genome_thick + ygap, join_thick, join_color)
                svg.drawLine(x2, top_buffer, x2, top_buffer + genome_thick, snp_thick, color2)
                svg.drawLine(x1, top_buffer + genome_thick + ygap, x1, top_buffer + 2 * genome_thick + ygap, snp_thick, color1)
            elif line.startswith('SV'):
                stuff1, q_name, pos1, pos2, r_name, pos3, pos4, b1, b2, anc_type, the_type, genes1, genes2, genes3, genes4, genes5, genes6, genes7, genes8, genes9, genes10 = line.split('\t')
                pos1, pos2, pos3, pos4 = map(int, (pos1, pos2, pos3, pos4))
                if the_type == 'deletion in query':
                    x1 = int(pos1 * 1.0 / max_width * fig_width) + left_buffer
                    x2 = int(pos2 * 1.0 / max_width * fig_width) + left_buffer
                    x3 = int(pos3 * 1.0 / max_width * fig_width) + left_buffer
                    x4 = int(pos4 * 1.0 / max_width * fig_width) + left_buffer
                    width = x4 - x3
                    if width < 1:
                        width = 1
                    y1 = top_buffer + genome_thick + blast_hit_overhang
                    y2 = top_buffer + genome_thick + ygap - blast_hit_overhang
                    svg.drawBlastHit(x1, y2, x2, y2, x3 + width + sv_thick/2, y1, x3 - sv_thick/2, y1, (0, 0, 0), 0, 0.4)
                    color = colourDictSV[the_type]
                    svg.drawOutRect(x3, top_buffer - blast_overhang, width, genome_thick + 2 * blast_overhang, color, color, sv_thick, 1, alpha2=0.6)
                elif the_type == 'tandem expansion in query':
                    x1 = int(pos1 * 1.0 / max_width * fig_width) + left_buffer
                    x2 = int(pos2 * 1.0 / max_width * fig_width) + left_buffer
                    x3 = int(pos3 * 1.0 / max_width * fig_width) + left_buffer
                    x4 = int(pos4 * 1.0 / max_width * fig_width) + left_buffer
                    y1 = top_buffer + genome_thick + blast_hit_overhang
                    y2 = top_buffer + genome_thick + ygap - blast_hit_overhang
                    width1 = x2 - x1
                    if width1 < 1:
                        width1 = 1
                    width2 = x4 - x3
                    if width2 < 1:
                        width2 = 1
                    svg.drawBlastHit(x1 - sv_thick/2, y2, x1 + width2 + sv_thick/2, y2, x3 + width2 + sv_thick/2, y1, x3 - sv_thick/2, y1, (0, 0, 0), 0, 0.4)
                    svg.drawBlastHit(x1 + width1 - width2 - sv_thick/2, y2, x1 + width1 + sv_thick/2, y2, x3 + width2 + sv_thick/2, y1, x3 - sv_thick/2, y1, (0, 0, 0), 0, 0.4)
                    color1, color2 = colourDictSV[the_type]
                    svg.drawOutRect(x1, top_buffer + genome_thick + ygap - blast_overhang, width1, genome_thick + 2 * blast_overhang, color1, color1, sv_thick, 1, alpha2=0.6)
                    svg.drawOutRect(x3, top_buffer - blast_overhang, width2, genome_thick + 2 * blast_overhang, color2, color2, sv_thick, 1, alpha2=0.6)
                elif the_type == 'insertion in query':
                    x1 = int(pos1 * 1.0 / max_width * fig_width) + left_buffer
                    x2 = int(pos2 * 1.0 / max_width * fig_width) + left_buffer
                    x3 = int(pos3 * 1.0 / max_width * fig_width) + left_buffer
                    x4 = int(pos4 * 1.0 / max_width * fig_width) + left_buffer
                    y1 = top_buffer + genome_thick + blast_hit_overhang
                    y2 = top_buffer + genome_thick + ygap - blast_hit_overhang
                    width = x2 - x1
                    if width < 1:
                        width = 1
                    svg.drawBlastHit(x1 - sv_thick/2, y2, x1 + width + sv_thick/2, y2, x4, y1, x3, y1, (0, 0, 0), 0, 0.4)
                    color = colourDictSV[the_type]
                    svg.drawOutRect(x1, top_buffer + genome_thick + ygap - blast_overhang, width, genome_thick + 2 * blast_overhang, color, color, sv_thick, 1, alpha2=0.6)
                elif the_type == 'tandem contraction in query':
                    x1 = int(pos1 * 1.0 / max_width * fig_width) + left_buffer
                    x2 = int(pos2 * 1.0 / max_width * fig_width) + left_buffer
                    x3 = int(pos3 * 1.0 / max_width * fig_width) + left_buffer
                    x4 = int(pos4 * 1.0 / max_width * fig_width) + left_buffer
                    width1 = x2 - x1
                    if width1 < 1:
                        width1 = 1
                    width2 = x4 - x3
                    if width2 < 1:
                        width2 = 1
                    y1 = top_buffer + genome_thick + blast_hit_overhang
                    y2 = top_buffer + genome_thick + ygap - blast_hit_overhang
                    svg.drawBlastHit(x1 - sv_thick/2, y2, x1 + width1 + sv_thick/2, y2, x3 + width2 + sv_thick/2, y1, x3 + width2 - width1 - sv_thick/2, y1, (0, 0, 0), 0, 0.4)
                    svg.drawBlastHit(x1 - sv_thick/2, y2, x1 + width1 + sv_thick/2, y2, x3 + width1 + sv_thick/2, y1, x3 - sv_thick/2, y1, (0, 0, 0), 0, 0.4)
                    color1, color2 = colourDictSV[the_type]
                    svg.drawOutRect(x1, top_buffer + ygap + genome_thick - blast_overhang, width1, genome_thick + 2 * blast_overhang, color2, color2, sv_thick, 1, alpha2=0.6)
                    svg.drawOutRect(x3, top_buffer - blast_overhang, width2, genome_thick + 2 * blast_overhang, color1, color1, sv_thick, 1, alpha2=0.6)
                elif the_type == 'insertion in query (duplicated ends)':
                    x1 = int(pos1 * 1.0 / max_width * fig_width) + left_buffer
                    x2 = int(pos2 * 1.0 / max_width * fig_width) + left_buffer
                    x3 = int(pos3 * 1.0 / max_width * fig_width) + left_buffer
                    x4 = int(pos4 * 1.0 / max_width * fig_width) + left_buffer
                    y1 = top_buffer + genome_thick + blast_hit_overhang
                    y2 = top_buffer + genome_thick + ygap - blast_hit_overhang
                    width1 = x2 - x1
                    if width1 < 1:
                        width1 = 1
                    width2 = x4 - x3
                    if width2 < 1:
                        width2 = 1
                    svg.drawBlastHit(x1 - width2 - sv_thick/2, y2, x1 + sv_thick/2, y2, x3 + width2 + sv_thick/2, y1, x3 - sv_thick/2, y1, (0, 0, 0), 0, 0.4)
                    svg.drawBlastHit(x1 + width1 - sv_thick/2, y2, x1 + width1 + width2 + sv_thick/2, y2, x3 + width2 + sv_thick/2, y1, x3 - sv_thick/2, y1, (0, 0, 0), 0, 0.4)
                    color1, color2 = colourDictSV[the_type]
                    svg.drawOutRect(x1 - width2, top_buffer + genome_thick + ygap - blast_overhang, width2, genome_thick + 2 * blast_overhang, color2, color2, sv_thick, 1, alpha2=0.6)
                    svg.drawOutRect(x1 + width1, top_buffer + genome_thick + ygap - blast_overhang, width2, genome_thick + 2 * blast_overhang, color2, color2, sv_thick, 1, alpha2=0.6)
                    svg.drawOutRect(x1, top_buffer + genome_thick + ygap - blast_overhang, width1, genome_thick + 2 * blast_overhang, color1, color1, sv_thick, 1, alpha2=0.6)
                    svg.drawOutRect(x3, top_buffer - blast_overhang, width2, genome_thick + 2 * blast_overhang, color2, color2, sv_thick, 1, alpha2=0.6)
                elif the_type == 'deletion in query (duplicated ends)':
                    x1 = int(pos1 * 1.0 / max_width * fig_width) + left_buffer
                    x2 = int(pos2 * 1.0 / max_width * fig_width) + left_buffer
                    x3 = int(pos3 * 1.0 / max_width * fig_width) + left_buffer
                    x4 = int(pos4 * 1.0 / max_width * fig_width) + left_buffer
                    y1 = top_buffer + genome_thick + blast_hit_overhang
                    y2 = top_buffer + genome_thick + ygap - blast_hit_overhang
                    width1 = x2 - x1
                    if width1 < 1:
                        width1 = 1
                    width2 = x4 - x3
                    if width2 < 1:
                        width2 = 1
                    svg.drawBlastHit(x1 - sv_thick/2, y2, x1 + width1 + sv_thick/2, y2, x3 + sv_thick/2, y1, x3 - width1 - sv_thick/2, y1, (0, 0, 0), 0, 0.4)
                    svg.drawBlastHit(x1 - sv_thick/2, y2, x1 + width1 + sv_thick/2, y2, x3 + width2 + width1 + sv_thick/2, y1, x3 + width2 - sv_thick/2, y1, (0, 0, 0), 0, 0.4)
                    color1, color2 = colourDictSV[the_type]
                    svg.drawOutRect(x1, top_buffer + genome_thick + ygap - blast_overhang, width1, genome_thick + 2 * blast_overhang, color2, color2, sv_thick, 1, alpha2=0.6)
                    svg.drawOutRect(x3 - width1, top_buffer - blast_overhang, width1, genome_thick + 2 * blast_overhang, color2, color2, sv_thick, 1, alpha2=0.6)
                    svg.drawOutRect(x3 + width2, top_buffer - blast_overhang, width1, genome_thick + 2 * blast_overhang, color2, color2, sv_thick, 1, alpha2=0.6)
                    svg.drawOutRect(x3, top_buffer - blast_overhang, width2, genome_thick + 2 * blast_overhang, color1, color1, sv_thick, 1, alpha2=0.6)
                elif the_type == 'Variable region':
                    x1 = int(pos1 * 1.0 / max_width * fig_width) + left_buffer
                    x2 = int(pos2 * 1.0 / max_width * fig_width) + left_buffer
                    x3 = int(pos3 * 1.0 / max_width * fig_width) + left_buffer
                    x4 = int(pos4 * 1.0 / max_width * fig_width) + left_buffer
                    y1 = top_buffer + genome_thick + blast_hit_overhang
                    y2 = top_buffer + genome_thick + ygap - blast_hit_overhang
                    width1 = x2 - x1
                    if width1 < 1:
                        width1 = 1
                    width2 = x4 - x3
                    if width2 < 1:
                        width2 = 1
                    svg.drawBlastHit(x1 - sv_thick/2, y2, x1 + width1 + sv_thick/2, y2, x3 + width2 +sv_thick/2, y1, x3-sv_thick/2, y1, (0, 0, 0), 0, 0.4)
                    color = colourDictSV[the_type]
                    svg.drawOutRect(x1, top_buffer + genome_thick + ygap - blast_overhang, width1, genome_thick + 2 * blast_overhang, color, color, sv_thick, 1, alpha2=0.6)
                    svg.drawOutRect(x3, top_buffer - blast_overhang, width2, genome_thick + 2 * blast_overhang, color, color, sv_thick, 1, alpha2=0.6)
                elif the_type == 'inversion':
                    x1 = int(pos1 * 1.0 / max_width * fig_width) + left_buffer
                    x2 = int(pos2 * 1.0 / max_width * fig_width) + left_buffer
                    x3 = int(pos3 * 1.0 / max_width * fig_width) + left_buffer
                    x4 = int(pos4 * 1.0 / max_width * fig_width) + left_buffer
                    y1 = top_buffer + genome_thick + blast_hit_overhang
                    y2 = top_buffer + genome_thick + ygap - blast_hit_overhang
                    width1 = x2 - x1
                    if width1 < 1:
                        width1 = 1
                    width2 = x4 - x3
                    if width2 < 1:
                        width2 = 1
                    svg.drawBlastHit(x1 - sv_thick/2, y2, x1 + width1 + sv_thick/2, y2, x3-sv_thick/2, y1, x3 + width2 +sv_thick/2, y1, (0, 0, 0), 0, 0.4)
                    color = colourDictSV[the_type]
                    svg.drawOutRect(x1, top_buffer + genome_thick + ygap - blast_overhang, width1, genome_thick + 2 * blast_overhang, color, color, sv_thick, 1, alpha2=0.6)
                    svg.drawOutRect(x3, top_buffer - blast_overhang, width2, genome_thick + 2 * blast_overhang, color, color, sv_thick, 1, alpha2=0.6)
                else:
                    print line.rstrip()
    svg.writesvg(out_file + '.svg')


parser = argparse.ArgumentParser()
parser.add_argument("-q", "--query_genbank", help="Genbank of query", metavar="query.gbk")
parser.add_argument("-r", "--reference_genbank", help="Genbank of reference.", metavar="reference.gbk")
parser.add_argument("-m", "--maf", help="multiple alignment file from Mugsy", metavar="mygenome.maf")
parser.add_argument("-n", "--number_of_genomes_in_maf", help="Number of genomes in multiple alignment", metavar="<int>")
parser.add_argument("-p", "--paml_rst", help="RST file produced by PAML", metavar="rst")
parser.add_argument("-a", "--ancestor_number", help="number of ancestor - get from Tree in rst file PAML outputs")
parser.add_argument("-o", "--out_file", help="where to output table and SVG")
parser.add_argument("-w", "--working_dir", help="Where to create nucmer output")
args = parser.parse_args()

if not args.paml_rst is None:
    anc_seq = get_ancestral_sequence(args.paml_rst, int(args.ancestor_number) - int(args.number_of_genomes_in_maf) - 1)
    msa = get_alignments(args.maf, args.number_of_genomes_in_maf)
else:
    anc_seq = None
    msa = None
genes1, seq1 = get_genes(args.query_genbank)
genes2, seq2 = get_genes(args.reference_genbank)
get_diff(args.query_genbank, args.reference_genbank, args.working_dir, args.out_file, msa, anc_seq, genes1, genes2, seq1, seq2)
q_name = args.query_genbank.split('/')[-1].split('.')[0]
r_name = args.reference_genbank.split('/')[-1].split('.')[0]
draw_diff(args.out_file, len(seq1), len(seq2), q_name, r_name, args.out_file)