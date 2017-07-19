import subprocess
import sys
import os



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


def run_nucmer(working_dir, r_file, q_file, seqDict, gene_dict, desc_dict):
    r_name = r_file.split('/')[-1].split('.')[0]
    q_name = q_file.split('/')[-1].split('.')[0]
    # subprocess.Popen('nucmer --breaklen=20 --prefix=' + working_dir + '/' + r_name + '_' + q_name + ' ' +
    #                  r_file + ' ' + q_file, shell=True, stderr=subprocess.PIPE).wait()
    # subprocess.Popen('delta-filter -g ' + working_dir + '/' + r_name + '_' + q_name + '.delta > ' +
    #                  working_dir + '/' + r_name + '_' + q_name + '.filter.delta', shell=True, stderr=subprocess.PIPE).wait()
    # subprocess.Popen('show-snps -Tlr ' + working_dir + '/' + r_name + '_' + q_name + '.filter.delta > ' + working_dir + '/' + r_name + '_' + q_name + '.snps',
    #                  shell=True, stderr=subprocess.PIPE).wait()
    with open(working_dir + '/' + r_name + '_' + q_name + '.snps') as snps:
        get_snp_lines = False
        out_list = []
        for line in snps:
            if line.startswith('[P1]'):
                get_snp_lines = True
            elif get_snp_lines:
                pos1, b1, b2, pos2, buff, dist, rr, rq, lenr, lenq, fr, tag, contig, name2 = line.split()
                mut_type = 'intergenic'
                aa_seq = 'none'
                for i in gene_dict[contig]:
                    start, stop, strand, gene, locus, seq, product = i
                    if start <= int(pos1) <= stop:
                        gene_seq = seqDict[contig][start-1:stop]
                        gene_seq_altered = seqDict[contig][start-1:int(pos1)-1] + b2 + seqDict[contig][int(pos1):stop]
                        if strand == '-':
                            gene_seq = reverse_compliment(gene_seq)
                            gene_seq_altered = reverse_compliment(gene_seq_altered)
                        aa_seq = translate_dna(gene_seq)
                        aa_seq_altered = translate_dna(gene_seq_altered)
                        if not '*' in aa_seq_altered:
                            mut_type = 'stop_loss'
                        elif '*' in aa_seq_altered[:-1]:
                            mut_type = 'stop_gain'
                        elif aa_seq == aa_seq_altered:
                            mut_type = 'synonymous'
                        else:
                            mut_type = 'nonsynonymous'
                        break
                if b1 == '.':
                    mut = 'ins' + b2
                    if mut_type != 'intergenic':
                        if len(b2) % 3 != 0:
                            mut_type = 'frameshift'
                        else:
                            mut_type = 'inframe'
                elif b2 == '.':
                    mut = 'del' + b1
                    if mut_type != 'intergenic':
                        if len(b1) % 3 != 0:
                            mut_type = 'frameshift'
                        else:
                            mut_type = 'inframe'
                else:
                    mut = b1 +  '>' + b2
                if mut_type == 'intergenic':
                    gene, locus, product = 'none', 'none', 'none'


                mut_name = contig + '.' + pos1.zfill(7) + '.' + mut
                desc_dict[mut_name] = (mut_type, gene, locus, product, aa_seq)
                out_list.append(mut_name)
    return out_list





def getSNVsSet(the_dir, ref, working_dir, pheno, ref_gbk, order_list):
    snv_dict = {}
    pheno_list = []
    with open(ref_gbk) as gbk:
        gene_dict = {}
        seqDict = {}
        getseq2 = False
        getseq = False
        getproduct = False
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
                product = 'none'
            elif line.startswith('     CDS '):
                startstop = line.split()[1]
                strand = '+'
                start, stop = map(int, startstop.split('..'))
                gene = 'none'
                product = 'none'
            elif line.startswith('                     /locus_tag'):
                locus_tag = line.split('"')[1]
            elif line.startswith('                     /gene='):
                gene = line.split('"')[1]
            elif getproduct:
                product += ' ' + line.rstrip().lstrip()
                if product.endswith('"'):
                    product = product[:-1]
                    getproduct = False
            elif line.startswith('                     /product='):
                product = line.split('"')[1]
                if not line.rstrip().endswith('"'):
                    product = product.rstrip()
                    getproduct = True
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
    descDict = {}
    the_order = []
    with open(order_list) as f:
        for line in f:
            the_order.append(line.rstrip())
    for a_file in the_order:
        with open(pheno) as f:
            f.readline()
            got_pheno = False
            for line in f:
                extract, heme, pmn_tsb, pmn_tcp, pbmc_tsb, pbmc_ycp = line.rstrip().split('\t')
                if extract in a_file:
                    got_pheno = True
                    pheno_list.append([a_file, heme, pmn_tsb, pmn_tcp, pbmc_tsb, pbmc_ycp])
                    break
        print a_file
        snv_list = run_nucmer(working_dir, ref, the_dir + '/' + a_file, seqDict, gene_dict, descDict)
        for i in snv_list:
            if i in snv_dict:
                snv_dict[i].add(a_file)
            else:
                snv_dict[i] = set([a_file])
    snv_list = list(snv_dict)
    snv_list.sort()
    out = open(working_dir + '/output.tsv', 'w')
    for num in range(6):
        out.write('\t\t\t\t\t')
        for i in pheno_list:
            out.write('\t' + i[num])
        out.write('\n')
    for i in snv_list:
        if len(snv_dict[i]) > 2:
            out.write(i + '\t' + '\t'.join(descDict[i]))
            for j in pheno_list:
                if j[0] in snv_dict[i]:
                    out.write('\t1')
                else:
                    out.write('\t0')
            out.write('\n')
try:
    os.makedirs(sys.argv[3])
except:
    pass


getSNVsSet(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])