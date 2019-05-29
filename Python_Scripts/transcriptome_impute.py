# work on example firstly
import os
import config
import multiprocessing as mp

plink = config.get_plink()
rawgenotype = config.get_rawgenotype()
output = config.get_output()
pythonscript = config.get_pythonscript()
weights = config.get_weights()
result = config.get_result()
rscript = config.get_rscript()


os.system("module load GCC/6.4.0-2.28  OpenMPI/2.1.1 R/3.4.3")
os.system("module load GCC/6.4.0-2.28 Python/3.6.3")

# prepare genotype file,convert plink format to dosage
# # firstly, separate the cleanchr_qc into each chromosome
for chr in range(1, 23):
    os.system("%s --bfile %s --noweb --chr %s --make-bed --out %schr%s" % (plink, rawgenotype, chr, output, chr))

# # parallel the conversion process


def conversion(chr):
    os.system("python %sconvert_plink_to_dosage.py -b %schr%s -p %s -o %schr" % (pythonscript, output, chr, plink, output))


def multicore():
    pool = mp.Pool()
    pool.map(conversion, range(1, 23))


multicore()

# prediction genetic expression based on whole blood prediction model
os.system(".%sPrediXcan.py --predict --dosages %s --samples %ssamples.txt --weights %s --output_prefix %swholeblood_pred" % (pythonscript, output, output, weights, result))

# association with phenotypes
