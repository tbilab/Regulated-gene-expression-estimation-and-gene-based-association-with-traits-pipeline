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
phenofile = config.get_phenofile()
outputprefix = config.get_outputprefix()


os.system("module load GCC/6.4.0-2.28  OpenMPI/2.1.1 R/3.4.3")
os.system("module load GCC/6.4.0-2.28 Python/3.6.3")

# prepare genotype file,convert plink format to dosage
# # firstly, separate the raw genotype data into each chromosome
def sepchr():
    for chr in range(1,23):
        os.system("%s --bfile %s --noweb --chr %s --make-bed --out %schr%s" % (plink,rawgenotype,chr,output,chr))

# # parallel the conversion process


def conversion(chr):
    os.system("python %sconvert_plink_to_dosage.py -b %schr%s -p %s -o %schr" % (pythonscript, output, chr, plink, output))


def multicore():
    pool = mp.Pool()
    pool.map(conversion, range(1, 23))


# prediction genetic expression based on whole blood prediction model
def prediction():
    os.system(".%sPrediXcan.py --predict --dosages %s --samples %ssamples.txt --weights %s --output_prefix %s" % (pythonscript, output, output, weights, outputprefix))


# association with phenotypes
#association, logistic regression
##due to the reason of permission denied caused by subprocess.call()
##os.system("python %sPrediXcan.py --assoc --pheno %sjak2_pheno --missing-phenotype -9 --pred_exp %sMEGA_predicted_expression.txt --logistic --output_prefix %sMEGA_wholeblood" % (rawpath, output, result, result))
def association():
    os.system("Rscript %sPrediXcanAssociation.R PRED_EXP_FILE %sMEGA_predicted_expression.txt PHENO_FILE %s MISSING_PHENOTYPE -9 TEST_TYPE logistic OUT %s_association.txt PHENO_COLUMN None PHENO_NAME None FILTER_FILE None FILTER_VAL None FILTER_COLUMN None" % (rscript, result, phenofile, outputprefix))

# plot
#plot and annotate the result
def annotate():
    os.system("Rscript %sannotate_plot.R %s 0.00005" % (rawpath, outputprefix))

#select a gene expression data by gene name from the individual level prediction data
def selectgene(outputfile,inputfile,ncolumn_gene):
    writePLGRKT = open(outputfile,"w")
    with open(inputfile) as Predictmodel:
        for line in Predictmodel:
            sline= line.split("\t")
            FID = sline[0]
            IID = sline[1]
            gene = sline[ncolumn_gene]
            writePLGRKT.write(FID + "\t" + IID + "\t" + gene + "\n")
    writePLGRKT.close()



#sepchr()
#multicore()
#prediction()
#association()
#annotate()
#selectgene(outputfile,inputfile,ncolumn_gene)