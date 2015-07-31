import sys
import time
import subprocess
import os

def vcflib_vcf2tsv(in_vcf, out_tsv, log_dir):
    ''' Converting vcf to tsv'''
    print "Converting vcf to tsv ...."

    ## checking inputs
    assert in_vcf
    assert out_tsv
    assert log_dir

    ## checking files
    assert os.path.isfile(in_vcf)
    assert os.path.isdir(log_dir)

    ## log files for standard out and error
    tsv_file = open(out_tsv,'w')
    stderr_file_name = log_dir + "/vcf2tsv"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder")
    stderr_file = open(stderr_file_name,'w')

    ## run command
    vcf2tsv_command = ["vcf2tsv","-g", in_vcf]
    subprocess.call(vcf2tsv_command, stdout=tsv_file, stderr=stderr_file)

    ## checking for output
    ### this does not check to make sure the file is not empty
    assert os.path.isfile(out_tsv)
    assert os.path.isfile(stderr_file_name)

    tsv_file.close(); stderr_file.close()