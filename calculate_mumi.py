import sys
import subprocess
import os
try:
    out = open(sys.argv[2], 'w')
except:
    sys.stdout.write('''
calculate_mumi.py
written by mjsull@gmail.com
usage: calculate_mumi.py <folder_name> <out_file.tsv>
where folder name is a folder containing all fasta files you want to compare (and only those files)
and out_file.tsv is the file where the table of mumi scores will be written

''')

x_names = []
lista = []
for i in os.listdir(sys.argv[1]):
    listb = []
    lista.append([i])
    for j in os.listdir(sys.argv[1]):
        listb.append(j)
        temp1 = open('seqa.fa', 'w')
        fasta = open(sys.argv[1] + '/' + i)
        seq = ''
        newseq = ''
        for line in fasta:
            if line.startswith('>'):
                if len(newseq) > len(seq):
                    seq = newseq
                newseq = ''
            else:
                newseq += line.rstrip()
        if len(newseq) > len(seq):
            seq = newseq
        temp1.write('>seqa\n' + seq)
        len1 = len(seq)
        temp1.close()
        temp1 = open('seqb.fa', 'w')
        fasta = open(sys.argv[1] + '/' + j)
        seq = ''
        newseq = ''
        for line in fasta:
            if line.startswith('>'):
                if len(newseq) > len(seq):
                    seq = newseq
                newseq = ''
            else:
                newseq += line.rstrip()
        if len(newseq) > len(seq):
            seq = newseq
        temp1.write('>seqa\n' + seq)
        len2 = len(seq)
        subprocess.Popen('mummer -mum -b -c -l 19 seqa.fa seqb.fa > tempmum', shell=True, stderr=subprocess.PIPE).wait()
        p = subprocess.Popen('perl give_mumi.pl tempmum -l1 ' + str(len1) + ' -l2 ' + str(len2) + ' > tempmumi', shell=True).wait()
        mumi = open('tempmumi')
        lista[-1].append(mumi.readline())
        mumi.close()
    print lista[-1]

out.write('genome\t' + '\t'.join(listb) + '\n')
for i in lista:
    out.write('\t'.join(i) + '\n')
