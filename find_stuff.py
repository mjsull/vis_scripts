import sys

with open(sys.argv[1]) as f, open(sys.argv[2], 'w') as o:
    ref_list = f.readline().rstrip().split('\t')[5:]
    heme_list = f.readline().rstrip().split('\t')[5:]
    pmn_tsb = f.readline().rstrip().split('\t')[5:]
    pmn_ycb = f.readline().rstrip().split('\t')[5:]
    pbmc_tsb = f.readline().rstrip().split('\t')[5:]
    pbmc_ycb = f.readline().rstrip().split('\t')[5:]
    heme_options = list(set(heme_list))
    pmn_tsb_options = list(set(pmn_tsb))
    pmn_ycb_options = list(set(pmn_ycb))
    pbmc_tsb_options = list(set(pbmc_tsb))
    pbmc_ycb_options = list(set(pbmc_ycb))
    for line in f:
        ref, mut_type, gene, locus, product = line.split('\t')[:5]
        pheno_list = line.rstrip().split('\t')[5:]
        out_list = []
        for k in heme_options:
            TP, FP, TN, FN = 0, 0, 0, 0
            for i, j in zip(heme_list, pheno_list):
                if j != '0' and i == k:
                    TP += 1
                elif j == '0' and i != k:
                    TN += 1
                elif j != '0' and i != k:
                    FP += 1
                elif j == '0' and i == k:
                    FN += 1
                else:
                    print 'dong'
            out_list.append((k, str(FP * 1.0 / (TP + TN + FP + FN)), str(FN * 1.0 / (TP + TN + FP + FN)), str(FP * 1.0 / (TP + TN + FP + FN) + FN * 1.0 / (TP + TN + FP + FN))))
        o.write('\t'.join(line.split('\t')[:5]))
        for k in out_list:
            o.write('\t' + '\t'.join(k))
        o.write('\n')

