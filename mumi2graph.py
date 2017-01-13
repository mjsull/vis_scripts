import networkx
import sys
import matplotlib.pyplot as plt
G = networkx.Graph()
getset = set()
with open(sys.argv[1]) as mumi:
    header = mumi.readline().split()[1:]
    for line in mumi:
        name = line.split()[0]
        best_edge_val = float('inf')
        best_edge = None
        for i, j in enumerate(line.split()[1:]):
            if float(j) < best_edge_val and name != header[i]:
                best_edge_val = float(j)
                best_edge = header[i]
            if float(j) <= 0.10:
                if name.startswith('MRSA'):
                    getset.add(header[i])
                G.add_edge(name, header[i], weight=float(j))
        G.add_edge(name, best_edge, weight=float(j))
print getset
print len(getset)
# networkx.draw(G, prog='neato')
# plt.show()
out = open(sys.argv[2], 'w')
out.write('''#!/bin/bash
#BSUB -J largeMulti
#BSUB -P acc_InfectiousDisease
#BSUB -q premium
#BSUB -n 1
#BSUB -R rusage[mem=500000]
#BSUB -W 144:00
#BSUB -R himem
#BSUB -m manda
#BSUB -o %J.stdout
#BSUB -eo %J.stderr
#BSUB -L /bin/bash

bash
source /hpc/users/sullim11/apps/mugsy_x86-64-v1r2.2/mugsyenv.sh
mugsy --directory /sc/orga/projects/InfectiousDisease/studies/sullim_assembly_finishing/MSSA_mugsy_86/ --prefix mygenomes ''')

for i in getset:
    print i
    out.write(' /hpc/users/sullim11/db/temp/' + i)
out.close()