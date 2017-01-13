#!/usr/bin/env python
# draw_coloured_tree.py   Written by: Mitchell Sullivan   mjsull@gmail.com
# organisation: Icahn School of Medicine - Mount Sinai
# Version 0.0.1 2016.01.19
# License: GPLv3

from ete3 import Tree, RectFace, AttrFace
import sys
from ete3 import NodeStyle
from ete3 import TreeStyle
from ete3 import Face
import argparse
import struct


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
    return "#%x%x%x" % (r/16,g/16,b/16)

# main function for drawing tree
def draw_tree(the_tree, colour, label, out_file, mlst, resistance, the_scale, extend, bootstrap, group_file):
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
    clade_cutoff = t.get_distance(the_leaves[0], the_leaves[-1]) /20
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
                    print 'ding'
                    if j in groups:
                        groups[j].append(i)
                    else:
                        groups[j] = [i]
        for i in groups:
            the_col = group_dict[i]
            print the_col
            print the_col
            style = NodeStyle()
            style['size'] = 0
            style["vt_line_color"] = the_col
            style["hz_line_color"] = the_col
            style["vt_line_width"] = 2
            style["hz_line_width"] = 2
            if len(groups[i]) == 1:
                print 'dong'
                ca = t.search_nodes(name=groups[i])[0]
                ca.set_style(style)
            else:
                print 'wang'
                ca = t.get_common_ancestor(groups[i])
                ca.set_style(style)
                tocolor = []
                for j in ca.children:
                    tocolor.append(j)
                while len(tocolor) > 0:
                    print 'dinga'
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
            print rgb1, rgb2
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
    if not mlst is None:
        mlst_dict = {}
        mlst_set = set()
        mlst_col = {'59':'#b76ea9',
                    '840':'#5db751',
                    '45':'#c356bf',
                    '231':'#b1b741',
                    '88':'#7368ce',
                    '5':'#d99a46',
                    '72':'#6990ce',
                    '7':'#cb5133',
                    '8':'#4baf91',
                    '496':'#cd4072',
                    '225':'#69843b',
                    '87':'#c96d70',
                    '105':'#9c7239'}
        with open(mlst) as pdb:
            pdb.readline()
            for line in pdb:
                extract_id, qc, browse, project, pathogen, clonal, hospital, unit, patient, alt_patient, collect_date, ass_id, mlst_no, clade, contigs, total, max_size, max_name, n50 = line.split(',')
                mlst_dict[qc] = mlst_no
                mlst_set.add(mlst_no)
        for n in t.traverse():
            if n.is_leaf():
                print n.name.split('.')[0]
                mlst_no = mlst_dict[n.name.split('.')[0][1:]]
                print mlst_no
                if mlst_no in mlst_col:
                    n.add_face(RectFace(10, 10, mlst_col[mlst_no], mlst_col[mlst_no]), column=1, position="aligned")
        print mlst_set
    if not resistance is None:
        resistance_dict = {}
        resistance_set = set()
        status_set = set()
        mlst_col = {'59':'#b76ea9',
                    '840':'#5db751',
                    '45':'#c356bf',
                    '231':'#b1b741',
                    '88':'#7368ce',
                    '5':'#d99a46',
                    '72':'#6990ce',
                    '7':'#cb5133',
                    '8':'#4baf91',
                    '496':'#cd4072',
                    '225':'#69843b',
                    '87':'#c96d70',
                    '105':'#9c7239'}
        with open(resistance) as res:
            res.readline()
            for line in res:
                blank, extract_id, pat_id, coll_date, procedure, pathogen, agent, a_class, MIC, status = line.rstrip().split(';')
                extract_id = extract_id[1:-1]
                agent = agent[1:-1]
                status = status[1:-1]
                if extract_id in resistance_dict:
                    if agent in resistance_dict[extract_id]:
                        print 'ding'
                        resistance_dict[extract_id][agent] = status
                    else:
                        resistance_dict[extract_id][agent] = status
                else:
                    resistance_dict[extract_id] = {agent:status}
                resistance_set.add(agent)
                status_set.add(status)
        resistance_set = set()
        status_set = set()
        for n in t.traverse():
            if n.is_leaf():
                extract = n.name.split('.')[0][10:17]
                if extract in resistance_dict:
                    for i in resistance_dict[extract]:
                        resistance_set.add(i)
                        status_set.add(resistance_dict[extract][i])
        res_list = list(resistance_set)
        print res_list
        face_width = 20
        for n in t.traverse():
            if n.is_leaf():
                print n.name
                extract = n.name.split('.')[0][10:17]
                if extract in resistance_dict:
                    for num, i in enumerate(res_list):
                        if i in resistance_dict[extract]:
                            if resistance_dict[extract][i] == 'Susceptible' or resistance_dict[extract][i] == 'NEG':
                                n.add_face(RectFace(face_width, face_width, '#008000', '#008000'), column=num+1, position="aligned")
                            elif resistance_dict[extract][i] == 'Intermediate':
                                n.add_face(RectFace(face_width, face_width, '#ff4500', '#ff4500'), column=num+1, position="aligned")
                            else:
                                n.add_face(RectFace(face_width, face_width, '#ff0000', '#ff0000'), column=num+1, position="aligned")
                        else:
                            n.add_face(RectFace(face_width, face_width, '#cccccc', '#cccccc'), column=num+1, position="aligned")

                # if mlst_no in mlst_col:
                #     n.add_face(RectFace(10, 10, mlst_col[mlst_no], mlst_col[mlst_no]), column=1, position="aligned")

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


parser = argparse.ArgumentParser()
parser.add_argument("-o", "--output_svg", help="SVG of tree", metavar="tree.svg")
parser.add_argument("-n", "--newick", help="newick tree file", metavar="tree.nw")
parser.add_argument("-c", '--color', action="store_true", default=False, help="Color tree")
parser.add_argument("-l", '--label', action="store_true", default=False, help="Add distance values")
parser.add_argument("-b", '--bootstrap', action="store_true", default=False, help="add bootstrap values")
parser.add_argument("-m", '--mlst', help="add MLST types from pathogendb", metavar="assemblies.csv")
parser.add_argument("-s", "--scale", type=float, default=5000, help="x scale of tree")
parser.add_argument("-r", '--resistance', help="add resistances from pathogendb", metavar="resistance.csv")
parser.add_argument("-g", '--group_file', help="file with groups of strains", metavar="Group.tsv")
parser.add_argument("-e", '--extend', help="extend tree branch", default=False, action="store_true")
args = parser.parse_args()

draw_tree(args.newick, args.color, args.label, args.output_svg, args.mlst, args.resistance, args.scale, args.extend, args.bootstrap, args.group_file)
