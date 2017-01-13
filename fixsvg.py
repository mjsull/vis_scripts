import sys
out = open(sys.argv[2], 'w')
wordDict = {
    'MRSA_pt035_N_078_ilm_reorient_chromosome':'pt035/Nares',
    'MRSA_pt053_N_164_ilm_reorient_chromosome':'pt053/Nares',
    'MRSA_pt073_B_085_ilm_reorient_chromosome':'pt073/Blood',
    'MRSA_pt158_B_196_ilm_reorient_chromosome':'pt158/Blood',
    'MRSA_pt152_N_628_ilm_reorient_chromosome':'pt152/Nares',
    'MRSA_pt108_B_128_ilm_reorient_chromosome':'pt108/Blood',
    'MRSA_pt045_B_045_ilm_reorient_chromosome':'pt045/Blood',
    'MRSA_pt053_B_054_ilm_reorient_chromosome':'pt053/Blood',
    'MRSA_pt035_B_027_ilm_reorient_chromosome':'pt035/Blood',
    'MRSA_pt135_N_545_ilm_reorient_chromosome':'pt135/Nares',
    'MRSA_pt117_F_468_ilm_reorient_chromosome':'pt117/Focus',
    'MRSA_pt152_B_187_ilm_reorient_chromosome':'pt152/Blood',
    'MRSA_pt152_F_629_ilm_reorient_chromosome':'pt152/Focus',
    'MRSA_pt117_B_143_ilm_reorient_chromosome':'pt117/Blood',
    'MRSA_pt135_F_546_ilm_reorient_chromosome':'pt135/Focus',
    'MRSA_pt060_B_061_ilm_reorient_chromosome':'pt060/Blood',
    'MRSA_pt135_B_165_ilm_reorient_chromosome':'pt135/Blood'
}
with open(sys.argv[1]) as infile:
    for line in infile:
        new_line = line
        for key in wordDict:
            new_line = new_line.replace(key, wordDict[key])
        out.write(new_line)