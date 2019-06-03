#!/usr/bin/env python
# ==========================to be edited by user


class global_var:
    # directory
    plink = " "        # full path of where the plink tool is
    rawgenotype = " "  # your raw genotype file
    output = " "  # output file path
    pythonscript = " "  # your raw path of the python script
    rscript = " "  # your raw path of the r script
    weights = " "  # full path to the prediction model database
    result = " "  # the path of your result
    phenofile = "" # the full path of your phenotype file
    outputprefix = "" # the prefix of the output file


def set_plink(plink):
    global_var.plink = plink


def get_plink():
    return global_var.plink


def set_rawgenotype(rawgenotype):
    global_var.rawgenotype = rawgenotype


def get_rawgenotype():
    return global_var.rawgenotype


def set_output(output):
    global_var.output = output


def get_output():
    return global_var.output


def set_pythonscript(pythonscript):
    global_var.pythonscript = pythonscript


def get_pythonscript():
    return global_var.pythonscript


def set_weights(weights):
    global_var.weights = weights


def get_weights():
    return global_var.weights


def set_result(result):
    global_var.result = result


def get_result():
    return global_var.result


def set_rscript(rscript):
    global_var.rscript = rscript


def get_rscript():
    return global_var.rscript

def set_phenofile(phenofile):
    global_var.phenofile = phenofile

def get_phenofile():
    return global_var.phenofile

def set_outputprefix(outputprefix):
    global_var.outputprefix = outputprefix

def get_outputprefix():
    return global_var.outputprefix