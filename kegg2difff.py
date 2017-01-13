import sys
import os
import math
from decimal import Decimal
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import FloatVector

def get_keggs(infile):
    out_list = []
    with open(infile) as f:
        for line in f:
            gene, kegg, desc = line.split('\t')[:3]
            if kegg != '':
                if gene == '':
                    gene = last_gene
                out_list.append((gene, kegg, desc))
                last_gene = gene
    return out_list


def get_diffs(folder):
    sorted_files = os.listdir(folder)
    sorted_files.sort()
    mod_genes = []
    for diffs in sorted_files:
        if diffs.endswith('N_diff'):
            with open(folder + '/' + diffs) as diff_file:
                diff_file.readline()
                for line in diff_file:
                    gene_group = []
                    type, q_name, pos1, pos2, r_name, pos3, pos4, b1, b2, anc_type, mut_type, genes1, genes2, genes3, genes4, genes5, genes6, genes7, genes8, genes9, genes10 = line.split('\t')
                    if mut_type == 'nonsyn_query':
                        genes = genes1.split(';')
                        genes = filter(lambda a: a != 'none', genes)
                        for i in genes:
                            gene_name = q_name[5:12] + '_' + i.split(',')[1]
                            mod_genes.append(gene_name)
                    elif mut_type == 'nonsyn_query_stop':
                        genes = genes1.split(';')
                        genes = filter(lambda a: a != 'none', genes)
                        for i in genes:
                            gene_name = q_name[5:12] + '_' + i.split(',')[1]
                            mod_genes.append(gene_name)
                    elif mut_type == 'syn_query':
                        pass
                        # genes = genes1.split(';')
                        # genes = filter(lambda a: a != 'none', genes)
                        # for i in genes:
                        #     gene_name = q_name[5:12] + '_' + i.split(',')[1]
                        #     mod_genes.append(gene_name)
                    elif mut_type == 'inframe_del_query':
                        genes = genes1.split(';')
                        genes = filter(lambda a: a != 'none', genes)
                        for i in genes:
                            gene_name = q_name[5:12] + '_' + i.split(',')[1]
                            mod_genes.append(gene_name)
                    elif mut_type == 'deletion_query':
                        genes = genes1.split(';')
                        genes = filter(lambda a: a != 'none', genes)
                        for i in genes:
                            gene_name = q_name[5:12] + '_' + i.split(',')[1]
                            mod_genes.append(gene_name)
                    elif mut_type == 'inframe_ins_query':
                        genes = genes1.split(';')
                        genes = filter(lambda a: a != 'none', genes)
                        for i in genes:
                            gene_name = q_name[5:12] + '_' + i.split(',')[1]
                            mod_genes.append(gene_name)
                    elif mut_type == 'insertion_query':
                        genes = genes1.split(';')
                        genes = filter(lambda a: a != 'none', genes)
                        for i in genes:
                            gene_name = q_name[5:12] + '_' + i.split(',')[1]
                            mod_genes.append(gene_name)
                    elif mut_type == 'syn_amb':
                        pass
                        # genes = genes1.split(';')
                        # genes = filter(lambda a: a != 'none', genes)
                        # for i in genes:
                        #     gene_name = q_name[5:12] + '_' + i.split(',')[1]
                        #     mod_genes.append(gene_name)
                    elif mut_type == 'syn_ref':
                        pass
                        # genes = genes1.split(';')
                        # genes = filter(lambda a: a != 'none', genes)
                        # for i in genes:
                        #     gene_name = q_name[5:12] + '_' + i.split(',')[1]
                        #     mod_genes.append(gene_name)
                    elif mut_type == 'nonsyn_amb':
                        genes = genes1.split(';')
                        genes = filter(lambda a: a != 'none', genes)
                        for i in genes:
                            gene_name = q_name[5:12] + '_' + i.split(',')[1]
                            mod_genes.append(gene_name)
                    elif mut_type == 'nonsyn_ref_stop':
                        pass
                        # genes = genes1.split(';')
                        # genes = filter(lambda a: a != 'none', genes)
                        # for i in genes:
                        #     gene_name = i.split(',')[0].split('_')[0]
                        #     if gene_name == 'none':
                        #         gene_name, ref_list = get_loci_group(i.split(',')[1], gen_folder, q_name, ref_list, homolog)
                        #     gene_group.append(gene_name)
                        #     out_dict = add_to_dict(q_name, gene_name, mut_type, out_dict)
                    elif mut_type == 'nonsyn_ref':
                        pass
                        # genes = genes1.split(';')
                        # genes = filter(lambda a: a != 'none', genes)
                        # for i in genes:
                        #     gene_name = i.split(',')[0].split('_')[0]
                        #     if gene_name == 'none':
                        #         gene_name, ref_list = get_loci_group(i.split(',')[1], gen_folder, q_name, ref_list, homolog)
                        #     gene_group.append(gene_name)
                        #     out_dict = add_to_dict(q_name, gene_name, mut_type, out_dict)
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
                        for i in genes:
                            gene_name = r_name[5:12] + '_' + i.split(',')[1]
                            mod_genes.append(gene_name)
                        genes = genes6.split(';')
                        genes = filter(lambda a: a != 'none', genes)
                        for i in genes:
                            gene_name = r_name[5:12] + '_' + i.split(',')[1]
                            mod_genes.append(gene_name)
                    elif mut_type == 'tandem contraction in query':
                        genes = genes1.split(';')
                        genes = filter(lambda a: a != 'none', genes)
                        for i in genes:
                            gene_name = q_name[5:12] + '_' + i.split(',')[1]
                            mod_genes.append(gene_name)
                    elif mut_type == 'deletion in query (duplicated ends)':
                        genes = genes2.split(';') + genes4.split(';')
                        genes = filter(lambda a: a != 'none', genes)
                        for i in genes:
                            gene_name = r_name[5:12] + '_' + i.split(',')[1]
                        genes = genes6.split(';')
                        genes = filter(lambda a: a != 'none', genes)
                        for i in genes:
                            gene_name = r_name[5:12] + '_' + i.split(',')[1]
                            mod_genes.append(gene_name)
                    elif mut_type == 'tandem expansion in query':
                        genes = genes1.split(';')
                        genes = filter(lambda a: a != 'none', genes)
                        for i in genes:
                            gene_name = q_name[5:12] + '_' + i.split(',')[1]
                            mod_genes.append(gene_name)
                            gene_name = i.split(',')[0].split('_')[0]
                    elif mut_type == 'insertion in query' or mut_type == 'plasmid_gain':
                        genes = genes1.split(';') + genes3.split(';')
                        genes = filter(lambda a: a != 'none', genes)
                        for i in genes:
                            gene_name = q_name[5:12] + '_' + i.split(',')[1]
                            mod_genes.append(gene_name)
                        genes = genes5.split(';')
                        genes = filter(lambda a: a != 'none', genes)
                        for i in genes:
                            gene_name = q_name[5:12] + '_' + i.split(',')[1]
                            mod_genes.append(gene_name)
                    elif mut_type == 'insertion in query (duplicated ends)':
                        genes = genes1.split(';') + genes3.split(';')
                        genes = filter(lambda a: a != 'none', genes)
                        for i in genes:
                            gene_name = q_name[5:12] + '_' + i.split(',')[1]
                            mod_genes.append(gene_name)
                        genes = genes5.split(';')
                        genes = filter(lambda a: a != 'none', genes)
                        for i in genes:
                            gene_name = q_name[5:12] + '_' + i.split(',')[1]
                            mod_genes.append(gene_name)
                    elif mut_type == 'inversion':
                        genes = genes5.split(';')
                        genes = filter(lambda a: a != 'none', genes)
                        for i in genes:
                            gene_name = q_name[5:12] + '_' + i.split(',')[1]
                            mod_genes.append(gene_name)
                    elif mut_type == 'Variable region':
                        genes = genes6.split(';')
                        genes = filter(lambda a: a != 'none', genes)
                        for i in genes:
                            gene_name = r_name[5:12] + '_' + i.split(',')[1]
                            mod_genes.append(gene_name)
                        genes = genes1.split(';') + genes3.split(';')
                        genes = filter(lambda a: a != 'none', genes)
                        for i in genes:
                            gene_name = q_name[5:12] + '_' + i.split(',')[1]
                            mod_genes.append(gene_name)
                        genes = genes5.split(';')
                        genes = filter(lambda a: a != 'none', genes)
                        for i in genes:
                            gene_name = q_name[5:12] + '_' + i.split(',')[1]
                            mod_genes.append(gene_name)
                    else:
                        print mut_type, 'dong dong dong'
    return mod_genes

def get_diffs_2(rna_file):
    mut_list = []
    with open(rna_file) as f:
        f.readline()
        for line in f:
            gene, chrom, length, sym, typeg, logfc, aveexpr, t, pval, adjpval, b = line.split('\t')
            if float(adjpval) <= 0.05:
                mut_list.append('pt053_N_' + gene)
    return mut_list


def get_brite(bf):
    out_dict = {}
    with open(bf) as brite_file:
        for line in brite_file:
            if line.startswith('A') or line.startswith('B') or line.startswith('C') or line.startswith('D') or line.startswith('E'):
                if line.startswith('A'):
                    upper_dict = {}
                    upper_dict['A'] = line.rstrip()
                elif 'PROKKA' in line.split()[1]:
                    gene = line.split()[1]
                    for i in upper_dict:
                        if gene in out_dict:
                            out_dict[gene].append(upper_dict[i])
                        else:
                            out_dict[gene] = [upper_dict[i]]
                else:
                    upper_dict[line[0]] = line.rstrip()
    return out_dict

def get_fischer(kegg_list, mut_list, brite_list):
    mut_set = set()
    for i in mut_list:
        mut_set.add(i)
    for i in kegg_list:
        if i[0] in brite_list:
            brite_list[i[0]].append(i[1])
        else:
            brite_list[i[0]] = [i[1]]
    kegg_set = set()
    for i in brite_list:
        if i in mut_set:
            for j in brite_list[i]:
                kegg_set.add(j)
    kegg_set = list(kegg_set)
    pval_list = []
    for i in kegg_set:
        a, b, c, d = 0, 0, 0, 0
        for j in brite_list:
            if 'pt053_B' in j:
                if i in brite_list[j]:
                    if j in mut_set:
                        a += 1
                    else:
                        c += 1
                else:
                    if j in mut_set:
                        b += 1
                    else:
                        d += 1
        pval = Decimal(math.factorial(a+b) * math.factorial(c+d) * math.factorial(a + c) * math.factorial(b + d)) / \
               Decimal(math.factorial(a) * math.factorial(b) * math.factorial(c) * math.factorial(d) * math.factorial(a+b+c+d))
        print i, a, b, c, d, pval
        pval_list.append(pval)
    stats = importr('stats')
    p_adjust = stats.p_adjust(FloatVector(pval_list), method = 'BY')
    print 'dang dang dang'
    for i in range(len(kegg_set)):
        if p_adjust[i] <= 0.05:
            print kegg_set[i], p_adjust[i]




kegg_list = get_keggs(sys.argv[1])
mut_list = get_diffs(sys.argv[2])
brite_list = get_brite(sys.argv[3])

get_fischer(kegg_list, mut_list, brite_list)