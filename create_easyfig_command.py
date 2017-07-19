import sys
import subprocess
import os



subprocess.Popen('makeblastdb -dbtype prot -out tempdb -in ' + sys.argv[2], shell=True).wait()
lenDict = {}
order = []
with open(sys.argv[2]) as f:
    for line in f:
        if line.startswith('>'):
            name = line.rstrip()[1:]
            lenDict[name] = 0
            order.append(name)
        else:
            lenDict[name] += len(line.rstrip())
command_string = []
stuff = os.listdir(sys.argv[1])
stuff.sort()
for i in stuff:
    with open(sys.argv[1] + '/' + i) as f, open('temp.fasta', 'w') as o:
        getseq = False
        for line in f:
            if line.startswith('LOCUS'):
                o.write('>' + line.split()[1] + '\n')
            elif line.startswith('ORIGIN'):
                getseq = True
            elif line.startswith('//'):
                getseq = False
            elif getseq:
                o.write(''.join(line.split()[1:]) + '\n')
    subprocess.Popen('blastx -query temp.fasta -db tempdb -out temp.blast -outfmt 6', shell=True).wait()
    hitDict = {}
    with open('temp.blast') as blast:
        for line in blast:
            query, subject, ident, length, mismatch, indel, qstart, qstop, rstart, rstop, eval, bitscore = line.split()
            ident = float(ident)
            length = int(length)
            if ident >= 90 and length >= 0.9 * lenDict[subject]:
                if subject in hitDict:
                    print 'fwahhhh'
                    sys.exit()
                hitDict[subject] = (int(qstart), int(qstop))
    if hitDict[order[0]][0] < hitDict[order[1]][0]:
        dir = ''
        start = min(hitDict[order[0]]) - 100
        stop = max(hitDict[order[1]]) + 100
    else:
        dir = 'R'
        start = min(hitDict[order[1]]) - 100
        stop = max(hitDict[order[0]]) + 100
    command_string.append(sys.argv[1] + i + ' ' + str(start) + ' ' + str(stop) + ' ' + dir)
    print command_string[-1]
print ' '.join(command_string)
