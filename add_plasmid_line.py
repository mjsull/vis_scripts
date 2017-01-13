import sys
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
        self.name = 'none'

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

def add_line(genbank, genbank1, genbank2, outfile, gain_loss):
    genes, seq = get_genes(genbank)
    r_name = genbank1.split('/')[-1][:-4]
    q_name = genbank2.split('/')[-1][:-4]
    out = open(outfile, 'w')
    if gain_loss == 'gain':
        cont_q = []
        for i in genes:
            cont_q.append(','.join([i.name, i.locus, i.strand, str(i.start) + '..' + str(i.stop), str(i.start) + '/' + str(i.stop - i.start)]))
        cont_r = ['none']
    else:
        cont_r = []
        for i in genes:
            cont_r.append(','.join([i.name, i.locus, i.strand, str(i.start) + '..' + str(i.stop), str(i.start) + '/' + str(i.stop - i.start)]))
        cont_q = ['none']
    out.write('\t'.join(map(str, ['SV', r_name, 'extrachrom', 'extrachrom', q_name, 'extrachrom', 'extrachrom', 'extrachrom', 'extrachrom', 'none', 'plasmid_' + gain_loss,
                     'none', 'none', 'none', 'none', ';'.join(cont_q), ';'.join(cont_r),
                     'none', 'none', 'none', 'none'])) + '\n')

add_line(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])