import sys
import time
import subprocess

def vcflib_vcf2tsv(in_vcf, out_tsv, log_dir):
    ''' Converting vcf to tsv'''
    print "Converting vcf to tsv ...."

    ## log files for standard out and error
    tsv_file = open(out_tsv,'w')
    stderr_file = open(log_dir + "/vcf2tsv"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')

    ## run command
    vcf2tsv_command = ["vcf2tsv","-g", in_vcf]
    subprocess.call(vcf2tsv_command, stdout=tsv_file, stderr=stderr_file)
    tsv_file.close(); stderr_file.close()