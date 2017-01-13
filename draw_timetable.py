import sys
import datetime
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





class patient:
    def __init__(self, mrn, name):
        self.mrn = mrn
        self.name = name
        self.extract_ids = []
        self.antibiotics = []
        self.stays = []
        self.events = []

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
        hour, minute, second = time.split(':')
    else:
        date = astring
        hour, minute, second = 12, 0, 0
    if '-' in date:
        year, month, day = date.split('-')
    else:
        month, day, year = date.split('/')
    month, day, year, hour, minute, second = map(int, [month, day, year, hour, minute, second])
    return datetime.datetime(year, month, day, hour, minute, second)



def load_patients(pat_file):
    out_dict = {'timeline':[]}
    patient_order = []
    with open(pat_file) as f:
        for line in f:
            if not line.startswith('#'):
                print line
                extract, date, erap, mrn, name, status = line.rstrip().split('\t')[:6]
                time = get_time(date)
                if mrn in out_dict:
                    out_dict[mrn].add_extract(extract, time, status)
                else:
                    if mrn == 'n/a':
                        out_dict['timeline'].append((extract, name, time, status))
                    else:
                        aninstance = patient(mrn, name)
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








def draw_timeline(pat_dict, orderlist, outfile, hosp_enc_loc, other_loc, snv_file, encounter_span):
    symbols = 'ox+sud^v'
    loc_color = {}
    color_len = len(hosp_enc_loc | other_loc)
    s_list = [0.3, 0.6, 0.7]
    l_list = [0.6, 0.8]
    other_loc = other_loc - hosp_enc_loc
    hosp_enc_loc = list(hosp_enc_loc)
    other_loc2 = list(other_loc)
    other_loc = list(other_loc)
    extract_color = {'outbreak':(150,50,50), 'precursor':(250,150,50), 'unrelated':(50,50,150), 'Culture negative':(150,50,150), 'Event':(50,250,50)}
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
    for num, i in enumerate(locations):
        h = num * 360 / color_len
        s = s_list[num%3]
        l = l_list[num%2]
        color = hsl_to_rgb(h, s, l)
        loc_color[i] = color
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
    stay_height = 40
    font_size = 36
    start_dt, end_dt = encounter_span
    first_tick = start_dt - datetime.timedelta(hours=start_dt.hour, minutes=start_dt.minute, seconds=start_dt.second)
    first_tick += datetime.timedelta(hours=24)
    extract_list = []
    for num, i in enumerate(orderlist):
        if num % 2 == 0:
            svg.drawOutRect(left_buffer, num * pat_height + top_buffer, width, pat_height, fill=(220, 220, 220), lt=0)
    count = 0
    while first_tick < end_dt:
        count += 1
        x = get_x_time(first_tick, start_dt, end_dt, width)
        if count % 5 == 0:
            svg.drawLine(left_buffer + x, top_buffer, left_buffer + x, len(orderlist) * pat_height + top_buffer, th=3)
            svg.writeString('Week ' + str(count), left_buffer + x, top_buffer - 10, font_size, rotate=-1,justify='right')
            svg.writeString(first_tick.isoformat()[:10], left_buffer + x, top_buffer - 10, font_size, rotate=-1,justify='right')
        else:
            svg.drawLine(left_buffer + x, top_buffer, left_buffer + x, len(orderlist) * pat_height + top_buffer, th=2)
        first_tick += datetime.timedelta(hours=24*7)
    strain_to_name_dict = {}
    extract_to_pat_and_time = {}
    for num, i in enumerate(orderlist):
        svg.writeString(i, left_buffer - 5, num * pat_height + pat_height/2 + font_size/3 + top_buffer, font_size, justify='right')
        svg.writeString(pat_dict[i].name, left_buffer + width + 5, num * pat_height + pat_height/2 + font_size/3 + top_buffer, font_size)
        for j in pat_dict[i].stays:
            start, end, loc = j
            startx = get_x_time(start, start_dt, end_dt, width)
            endx = get_x_time(end, start_dt, end_dt, width)
            color = loc_color[loc]
            if start_dt <= start <= end <= end_dt:
                svg.drawOutRect(startx + left_buffer, num * pat_height + top_buffer + (pat_height - stay_height) / 2, endx - startx, stay_height, fill=color, lt=0)
        for j in pat_dict[i].antibiotics:
            time, antibiotic = j
            x = get_x_time(time, start_dt, end_dt, width)
            color = ab_color[antibiotic]
            if start_dt <= time <= end_dt:
                svg.drawSymbol(x + left_buffer, top_buffer + num * pat_height + pat_height/2 + stay_height/2 + 7, 10, color, 's', lt=0)
        for j in pat_dict[i].events:
            time, what, loc = j
            x = get_x_time(time, start_dt, end_dt, width)
            color = loc_color[loc]
            symbol = event_dict[what]
            if start_dt <= time <= end_dt:
                svg.drawSymbol(x + left_buffer, top_buffer + num * pat_height + 10, 10, color, symbol, lt=0)
        for j in pat_dict[i].extract_ids:
            id, time, status = j
            extract_to_pat_and_time[id] = (i, time)
            strain_to_name_dict[id] = pat_dict[i].name
            if (status == 'outbreak' or status == 'precursor') and '.' in id:
                extract_list.append((time, id))
            x = get_x_time(time, start_dt, end_dt, width)
            color = extract_color[status]
            if start_dt <= time <= end_dt:
                if '.' in id:
                    svg.drawSymbol(x + left_buffer, top_buffer +  num * pat_height + pat_height/2, stay_height, color, 'o')
                elif id == 'Surveillance':
                    svg.drawSymbol(x + left_buffer, top_buffer +  num * pat_height + pat_height/2, stay_height, color, 's')
                else:
                    svg.drawSymbol(x + left_buffer, top_buffer +  num * pat_height + pat_height/2, stay_height, color, 'x')
    lastx = None
    svg.writeString('timeline', left_buffer - 5, top_buffer + num * pat_height + pat_height/2 + pat_height + font_size/3, font_size, justify='right')
    svg.drawLine(left_buffer, top_buffer + num * pat_height + pat_height/2 + pat_height, left_buffer + width, top_buffer + num * pat_height + pat_height/2 + pat_height, 10)
    for i in pat_dict['timeline']:
        extract, name, time, status = i
        strain_to_name_dict[extract] = name
        if (status == 'outbreak' or status == 'precursor') and '.' in extract:
            extract_list.append((time, extract))
        x = get_x_time(time, start_dt, end_dt, width)
        color = extract_color[status]
        if start_dt <= time <= end_dt:
            if name == 'Environmental':
                symbol = 'o'
            elif name == 'Staff culture':
                symbol = 's'
            if x == lastx:
                mod += 1
                svg.drawSymbol(x + left_buffer, top_buffer + num * pat_height + pat_height/2 + pat_height + stay_height*mod, stay_height, color, symbol)
            else:
                svg.drawSymbol(x + left_buffer, top_buffer + num * pat_height + pat_height/2 + pat_height, stay_height, color, symbol)
                lastx = x
                mod = 0
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
        print i
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
    print extract_list
    print ordered_extract_list
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
            print count
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
    for num, i in enumerate(hosp_enc_loc):
        svg.drawOutRect(left_buffer, leg_start + pat_height * num, stay_height * 2, stay_height, fill=loc_color[i], lt=0)
        svg.writeString(i, left_buffer + stay_height * 2 + 10, leg_start + pat_height * num + stay_height, font_size)
    for num, i in enumerate(other_loc2):
        svg.drawOutRect(left_buffer + 1000, leg_start + pat_height * num, stay_height, stay_height, fill=loc_color[i], lt=0)
        svg.writeString(i, left_buffer + stay_height * 1 + 10 + 1000, leg_start + pat_height * num + stay_height, font_size)
    for num, i in enumerate(event_dict):
        svg.drawSymbol(left_buffer + 2000, leg_start + pat_height * num + pat_height/3, 30, (100,100,100), event_dict[i], lt=0)
        svg.writeString(i, left_buffer + stay_height * 1 + 10 + 2000, leg_start + pat_height * num + stay_height, font_size)
    for num, i in enumerate(ab_color):
        svg.drawOutRect(left_buffer + 2500, leg_start + pat_height * num, stay_height, stay_height, fill=ab_color[i], lt=0)
        svg.writeString(i, left_buffer + stay_height * 1 + 10 + 2500, leg_start + pat_height * num + stay_height, font_size)
    for num, i in enumerate(base_col):
        svg.drawOutRect(left_buffer + width + 20,  top_buffer + (len(pat_dict) + 11) * pat_height + 5 + num * stay_height, stay_height * 2, stay_height, fill=base_col[i], lt=0)
        svg.writeString(i, left_buffer + width + 40 + stay_height*2, top_buffer + (len(pat_dict) + 11) * pat_height + 5 + num * stay_height + stay_height, font_size)




    print extract_list
    svg.writesvg(outfile)



pat_dict, pat_order = load_patients(sys.argv[1])
hosp_enc_loc, other_loc, encounter_span = get_events(pat_dict, sys.argv[2])
get_antibiotics(pat_dict, sys.argv[3])
try:
    start_time = get_time(sys.argv[6])
except IndexError:
    start_time = encounter_span[0]
try:
    end_time = get_time(sys.argv[7])
except IndexError:
    end_time = encounter_span[1]
snv_file = sys.argv[5]
draw_timeline(pat_dict, pat_order, sys.argv[4], hosp_enc_loc, other_loc, snv_file, (start_time, end_time))